#!/usr/bin/env bash
#===============================================================================
#
# Generic python virtual env bootstrap utility
#
# USAGE:
#   source ./dev-bootstrap.sh [MAJOR.MINOR]
#
# If an argument is provided, it is interpretted as a Python Major.minor pair.
#
# EXAMPLE: initializing with default python (3.8)
#   source ./dev-bootstrap.sh
#
# EXAMPLE: initializing with python 3.7
#   source ./dev-bootstrap.sh 3.7
#
# This script attempts to be reentrant and not pollute the shell environment.
# For more info, see:
# - https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html
#-------------------------------------------------------------------------------

#==========================================================
# Bash Options:
#----------------------------------------------------------
# By default, don't automatically export vars or functions:
set +a

#==========================================================
# Globals:
#----------------------------------------------------------

# Python related:
PYTHON3_VERSION_OUTPUT="$( ${PYTHON3:-"python3"} --version )"
PYTHON3_VERSION_FULL="${PYTHON3_VERSION:-"${PYTHON3_VERSION_OUTPUT##* }"}"
PYTHON3_VERSION="${PYTHON3_VERSION:-"${PYTHON3_VERSION_FULL%.*}"}"
PYTHON3="${PYTHON3:-"python${PYTHON3_VERSION}"}"
PIP3="${PIP3:-"pip${PYTHON3_VERSION}"}"

# Homebrew:
BREW_PYTHON="python@${PYTHON3_VERSION}"

# poast specific:
poast_GIT_ROOT="$( git rev-parse --show-toplevel 2>/dev/null )"
poast_ROOT="${poast_GIT_ROOT:-"${PWD}"}"
poast_VENV="${PIP_VENV:-"${poast_ROOT}/.venv${PYTHON3_VERSION}"}"
poast_PYTHON_BINDIR="/usr/local/opt/${BREW_PYTHON}/bin"
poast_GIT_HOOKS="${poast_GIT_HOOKS:-"${poast_ROOT}/util/hooks"}"

# Logs + misc:
PIP_LOG="${PIP_LOG:-"$( mktemp )"}"


#==========================================================
# Utility:
#----------------------------------------------------------
__poast_init_log_err() {
    echo -e "\e[00;03;31mERROR: $@\e[00m" >&2
    deactivate >/dev/null 2>&1
    return 1
}

__poast_init_log_info() {
    echo -e "\e[00;34;02mINFO: \e[00m$@\e[00m" >&2
}

# Run a command, logging the path and arguments
__poast_init_run_cmd() {
    local cmd
    cmd="$1" ; shift
    echo -e "\e[00;34;02mEXEC: \e[00;01;32m${cmd} \e[00;32m$@\e[00m" >&2
    ${cmd} "$@"
}

__poast_init_prompt() {
    echo -en "\e[00;03;32m$@ \e[00m[Y/n]: " >&2
    local answer
    read answer

    if [ "x${answer}" != "xn" ]; then
        return 0
    else
        return 1
    fi
}

#==========================================================
# Checks:
#----------------------------------------------------------
# Get the python version as major.minor:
__poast_init_get_python_Mm() {
    local python_version version_info
    python_version="$( python3 --version )"
    version_info="${python_version##* }"
    echo "${version_info%.*}"
}

__poast_init_ensure_python3_path() {
    __poast_init_log_info "Ensure \"${poast_PYTHON_BINDIR}\" is in \$PATH"
    local poast_pypath
    poast_pypath="$( tr ':' '\n' <<< "${PATH}" | grep "${BREW_PYTHON}" )"
    if [ -z "${poast_pypath}" ]; then
        __poast_init_log_info "Adding \"${poast_PYTHON_BINDIR}\" to PATH"
        set -a
        export PATH="${poast_PYTHON_BINDIR}:${PATH}"
        set +a
    fi
}

__poast_init_ensure_python3() {
    local py_version
    __poast_init_ensure_python3_path
    __poast_init_log_info "Ensure python is present"
    py_version="$( __poast_init_run_cmd "${PYTHON3}" --version 2>/dev/null )"

    if [ "x${py_version}" == "x" ]; then
        __poast_init_log_info "${PYTHON3} not found. Installing ${BREW_PYTHON}..."
        __poast_init_run_cmd brew install "${BREW_PYTHON}"

        # Remove any venv created with an older python:
        rm -rf "${poast_VENV}"
    else
        __poast_init_log_info "Found: ${py_version}"
    fi
}

__poast_init_venv_deactivate() {
    __poast_init_log_info "Check to see if venv is active..."
    if [ -n "${VIRTUAL_ENV}" ]; then
        __poast_init_log_info "Deactivating current venv: \"${VIRTUAL_ENV}\""
        __poast_init_run_cmd deactivate
    else
        __poast_init_log_info "No active venv found"
    fi
}

__poast_init_venv_create() {
    __poast_init_log_info "Ensure virtualenv is present"
    if [ ! -d "${poast_VENV}" ]; then
        __poast_init_log_info "Creating virtual environment"
        __poast_init_run_cmd "${PYTHON3}" -m venv "${poast_VENV}"
        if [ $? -ne 0 ]; then
            __poast_init_log_err "Unable to create virtualenv"
            return 1
        fi
    fi
}

__poast_init_venv_activate() {
    __poast_init_log_info "Activating virtualenv ${poast_VENV}"
    local venv_status
    set -a
    __poast_init_run_cmd source "${poast_VENV}/bin/activate"
    venv_status=$?
    set +a

    if [ ${venv_status} -ne 0 ]; then
        __poast_init_log_err "Unable to activate virtualenv"
        return 1
    else
        # Unless POAST_RELATIE_PATH == false, allow importing from the git root:
        if [ "x${POAST_RELATIVE_PATH}" != "xfalse" ]; then
            export PYTHONPATH="${PYTHONPATH}:${poast_GIT_ROOT}"
        fi
    fi
}

__poast_init_venv_bootstrap() {
    __poast_init_venv_deactivate
    __poast_init_venv_create
    __poast_init_venv_activate
}

__poast_init_venv_confirm() {
    local venv_version
    venv_version="$( __poast_init_get_python_Mm )"
    if [ "x${venv_version}" == "x${PYTHON3_VERSION}" ]; then
        __poast_init_log_info "virtualenv python version confirmed (${venv_version})"
        return
    fi

    __poast_init_log_err "An existing virtual env is present with ${venv_version} (need: ${PYTHON3_VERSION})."
    if __poast_init_prompt "Okay to remove and replace it?" ; then
        __poast_init_venv_deactivate
        __poast_init_run_cmd rm -r "${poast_VENV}"
        __poast_init_venv_bootstrap
    else
        return 1
    fi
}

__poast_init_dep_install() {
    __poast_init_log_info "Installing requirements (install log: \"${PIP_LOG}\")"
    #__poast_init_log_info "Ensuring pip is up to date"
    #__poast_init_run_cmd "${PIP3}" install --upgrade pip >> "${PIP_LOG}"

    if [ -r requirements_dev.txt ] ; then
        __poast_init_log_info "Installing dev requirements"
        __poast_init_run_cmd "${PIP3}" install -r requirements_dev.txt >> "${PIP_LOG}"
    fi

    if [ -r requirements.txt ] ; then
        __poast_init_log_info "Installing runtime requirements"
        __poast_init_run_cmd "${PIP3}" install -r requirements.txt >> "${PIP_LOG}"
    fi
}

__poast_init_add_git_hooks() {
    if [ -d "${poast_GIT_HOOKS}" ]; then
        __poast_init_log_info "Adding git hooks to the repo"

        local hook
        for hook in $( ls "${poast_GIT_HOOKS}" ); do
            __poast_init_log_info "Installing \"${hook}\" git hook"
            __poast_init_run_cmd cp ${poast_ROOT}/util/hooks/${hook} ./.git/hooks/${hook}
            __poast_init_run_cmd chmod +x .git/hooks/${hook}
        done
    fi
}

# HACK: avoid polluting the shell environment.
# Unset anything that starts with "__poast":
__poast_init_fn_cleanup() {
    local poast_fn
    local -a poast_fns

    poast_fns=($( declare -F | grep '\<__poast' | awk '{ print $3 }' ))
    for poast_fn in ${poast_fns[@]}; do
        unset -f "${poast_fn}"
    done
}

__poast_init_main() {
    __poast_init_ensure_python3 \
        && __poast_init_venv_bootstrap \
        && __poast_init_venv_confirm \
        && __poast_init_dep_install \
        && __poast_init_add_git_hooks \
        || __poast_init_log_err "Repo init failed..."
}

# Main:
trap __poast_init_fn_cleanup EXIT
__poast_init_main
set -a

# TODO: script summary:
# grep '^\w\w*()' ${0} | sed 's/ .*//g'

# EOF

