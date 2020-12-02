"""Console script for poast."""
import sys
import click
import yaml
from .spec import (
    OpenApiObject,
    MalformedDocumentException,
)


@click.command()
@click.version_option()
@click.option('--openapi-spec', type=click.Path(), envvar='OPENAPI_SPEC',
              default=None, help='Path to app OpenAPI Spec')
@click.option('--validate/--no-validate', default=True,
              help="Validate the loaded document")
@click.option(
    '--resolve-refs/--no-resolve-refs', default=False,
    help="Resolve document references")
@click.option('--show-unset/--no-show-unset', default=False,
              help="Show unset fields")
@click.option('--show-paths/--no-show-paths', default=False,
              help="Show document paths")
@click.option(
    '--show-attrs/--no-show-attrs', default=False,
    help="Show document attributes")
def main(
    openapi_spec, validate, resolve_refs, show_unset, show_paths,
        show_attrs):
    """Test OpenAPI Parser"""

    if openapi_spec is not None:
        try:
            doc = OpenApiObject(openapi_spec, resolve_refs=resolve_refs)
            if validate:
                doc.validate()

            print(f'\n\n---\n# {openapi_spec}:\n')
            print(yaml.dump(doc.value()))

            if show_paths:
                def print_by_path(obj):
                    py_val = obj.value(show_unset)

                    # Don't print full data for container types:
                    if isinstance(py_val, dict):
                        py_val = '{...}'
                    elif isinstance(py_val, list):
                        py_val = '[...]'

                    print('# path: {}: {} ({})'.format(
                        obj.doc_path, py_val, obj.openapi_type))

                print("\n# Elements by path:")
                doc.accept(print_by_path)

            if show_attrs:
                t_set = set()

                def attr_by_path(obj):
                    if obj.openapi_type not in t_set:
                        t_set.add(obj.openapi_type)
                        print(
                            f'#\n# Attributes for type {obj.openapi_type}:')
                        for attr_name in dir(obj):
                            attr_val = getattr(obj, attr_name)
                            if callable(attr_val):
                                suffix = '()'
                            else:
                                suffix = ''
                            # attr_doc = attr_val.__doc__
                            print(f'#   - {attr_name}{suffix}')

                print("\n# Elements by path:")
                doc.accept(attr_by_path)
        except MalformedDocumentException as e:
            print(str(e))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
