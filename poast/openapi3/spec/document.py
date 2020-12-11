"""
This module defines all of the concrete OpenApi 3.0 document objects.

.. note:: All of the object types here are defined in the
    `OpenAPI 3.0.3 specification <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md>`_
"""

import re
import string

from .model.exceptions import (
    MalformedDocumentException,
    InvalidFieldValueException,
)

from .util import load_yaml

from .model.baseobj import OpenApiBaseObject
from .model.reference import ReferenceObject

from .model.primitives import (
    OpenApiInteger,
    OpenApiNumber,
    OpenApiString,
    OpenApiBoolean,
    OpenApiAny,
)

from .model.containers import (
    OpenApiList,
    OpenApiMap,
)

from .model.field import OpenApiFieldSpec as _field
from .model.field import OpenApiFieldUnion as _union

from .validation import (
    require,
    require_value,
    required,
    in_range,
    is_url,
    is_email,
)

# --------------------------------------------------------------------------
# Object Definitions:
# --------------------------------------------------------------------------


class InfoObject(OpenApiBaseObject):
    """
    .. seealso:: `InfoObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#infoObject>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("title", OpenApiString),
            _field("description", OpenApiString),
            _field("termsOfService", OpenApiString),
            _field("contact", ContactObject),
            _field("license", LicenseObject),
            _field("version", OpenApiString),
        )

    @required('title')
    @required('version')
    def _validate(self):
        """Validation is 3.0.3 compliant"""
        pass


class ContactObject(OpenApiBaseObject):
    """
    .. seealso:: `ContactObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#contactObject>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("name", OpenApiString),
            _field("url", OpenApiString),
            _field("email", OpenApiString),
        )

    @is_url('url')
    @is_email('email')
    def _validate(self):
        """Validation is 3.0.3 compliant"""
        pass


class LicenseObject(OpenApiBaseObject):
    """
    .. seealso:: `LicenseObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#licenseObject>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("name", OpenApiString),
            _field("url", OpenApiString),
        )

    @required('name')
    @is_url('url')
    def _validate(self):
        """Validation is 3.0.3 compliant"""
        pass


class ServerObject(OpenApiBaseObject):
    """
    .. seealso:: `ServerObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#serverObject>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("url", OpenApiString),
            _field("description", OpenApiString),
            _field(
                "variables", OpenApiMap.of(ServerVariableObject)),
        )

    @required('url')
    @is_url('url')
    def _validate(self):
        """Validation is 3.0.3 compliant"""
        pass


class ServerVariableObject(OpenApiBaseObject):
    """
    .. seealso:: `ServerVariableObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#serverVariableObject>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            # Empty list not allowed; defaults to None.
            _field("enum", OpenApiList.of(OpenApiString)),
            _field("default", OpenApiString),
            _field("description", OpenApiString),
        )

    @required('default')
    def _validate(self):
        """Validation is 3.0.3 compliant"""
        pass


class ComponentsObject(OpenApiBaseObject):
    """
    .. seealso:: `ComponentsObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#componentsObject>`_
    """
    KEY_REGEX = r'^[a-zA-Z0-9\.\-_]+$'
    KEY_CONSTRAINT = re.compile(KEY_REGEX)

    @classmethod
    def _obj_spec(cls):
        return (
            _field("schemas", OpenApiMap.of(SchemaObject)),
            _field("responses", OpenApiMap.of(ResponseObject)),
            _field("parameters", OpenApiMap.of(ParameterObject)),
            _field("examples", OpenApiMap.of(ExampleObject)),
            _field(
                "requestBodies", OpenApiMap.of(RequestBodyObject)),
            _field("headers", OpenApiMap.of(HeaderObject)),
            _field("securitySchemes",
                   OpenApiMap.of(SecuritySchemeObject)),
            _field("links", OpenApiMap.of(LinkObject)),
            _field("callbacks", OpenApiMap.of(CallbackObject)),
        )

    def _validate(self):
        """Validation is 3.0.3 compliant"""
        # Keys for each of the nested dictionaries must match the regex:
        # "^[a-zA-Z0-9\.\-_]+$"
        for field_name in self._field_names():
            field_val = self[field_name]
            if field_val is None:
                return

            for key in field_val:
                self._validate_key(field_name, key)
        return

    def _validate_key(self, field_val, key):
        if not self.KEY_CONSTRAINT.match(key):
            raise InvalidFieldValueException(
                self, field_val,
                f'keys must match: "{self.KEY_REGEX}"; got: "{key}"')


class PathsObject(OpenApiMap):
    """
    .. seealso:: `PathsObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#pathsObject>`_
    """

    def __init__(self, data, doc_path):
        super().__init__(data, doc_path, PathItemObject)

    def _validate(self):
        """Validation is 3.0.3 compliant"""
        # 1. All operationIds defined by the API must be unique.
        # 2. No two paths can have the same general form, even if the parameter
        #    names are different, e.g.: "/pets/{id}" and "/pets/{petId}" are
        #    considered identical and invalid.
        paths = {}
        op_ids = {}
        for uri_path in self:
            if not uri_path.startswith('/'):
                raise MalformedDocumentException(self, uri_path,
                        "Paths must begin with '/'")

            path_key = self._get_validation_path_key(uri_path)

            if path_key in paths:
                other_path = self[paths[path_key]]
                raise MalformedDocumentException(
                    self, uri_path, f'conflicts with "{other_path.doc_path}"')
            else:
                paths[path_key] = uri_path

            self._validate_unique_ops(op_ids, uri_path)

    def _get_validation_path_key(self, uri_path):
        param_num = 1
        parts = []
        for text, name, spec, conv in string.Formatter().parse(uri_path):
            parts.append(text)
            if name:
                parts.append(f'param{param_num}')
                param_num += 1
        return ''.join(parts)

    def _validate_unique_ops(self, op_ids, uri_path):
        path_item = self[uri_path]
        for field_name in path_item:
            op_obj = path_item[field_name]
            if not isinstance(op_obj, OperationObject):
                continue

            op_id = op_obj.get('operationId', None)
            if op_id is None:
                continue

            other_op = op_ids.get(op_id, None)
            if other_op is not None:
                raise MalformedDocumentException(
                    self[uri_path],
                    op_id, f'conflicts with {other_op.doc_path}')
            else:
                op_ids[op_id] = op_obj
        return


# Validation is 3.0.3 compliant (i.e. no validation required)
class PathItemObject(OpenApiBaseObject):
    """
    .. seealso:: `PathItemObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#pathItemObject>`_

    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("summary", OpenApiString),
            _field("description", OpenApiString),
            _field("get", OperationObject),
            _field("put", OperationObject),
            _field("post", OperationObject),
            _field("delete", OperationObject),
            _field("options", OperationObject),
            _field("head", OperationObject),
            _field("patch", OperationObject),
            _field("trace", OperationObject),
            _field("servers", OpenApiList.of(ServerObject)),
            _field(
                "variables", OpenApiMap.of(ServerVariableObject)),
        )


class OperationObject(OpenApiBaseObject):
    """
    .. seealso:: `OperationObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#operationObject>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("tags", OpenApiList.of(OpenApiString)),
            _field("summary", OpenApiString),
            _field("description", OpenApiString),
            _field("externalDocs", ExternalDocumentationObject),
            _field("operationId", OpenApiString),
            _field("parameters", OpenApiList.of(ParameterObject), []),
            _field("requestBody", RequestBodyObject),
            _field("responses", ResponsesObject),
            _field("callbacks", OpenApiMap.of(CallbackObject)),
            _field("deprecated", OpenApiBoolean, False),
            _field("security", OpenApiList.of(
                SecurityRequirementObject), []),
            _field("servers", OpenApiList.of(ServerObject)),
        )

    @required('responses')
    def _validate(self):
        """Validation is 3.0.3 compliant"""
        unique_params = {}
        for param in self['parameters']:
            param_name = str(param['name'])
            param_in = str(param['in'])
            param_key = f'{param_name} in {param_in}'

            other_param = unique_params.get(param_key, None)
            if other_param is not None:
                raise MalformedDocumentException(
                    param, param_key,
                    f'is a duplicate of {other_param.doc_path}')
            else:
                unique_params[param_key] = param
        return


class ExternalDocumentationObject(OpenApiBaseObject):
    """
    .. seealso:: `ExternalDocumentationObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#externalDocumentationObject>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("description", OpenApiString),
            _field("url", OpenApiString),
        )

    @required('url')
    @is_url('url')
    def _validate(self):
        """Validation is 3.0.3 compliant"""
        pass


class ParameterObject(OpenApiBaseObject):
    """
    .. seealso::
     - `ParameterObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#parameterObject>`_
     - `Style-values <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#style-values>`_

    TODO: context-dependent default values
    TODO: serialization & styles
    """
    @classmethod
    def _obj_spec(cls):
        return (
            # Fixed Fields:
            _field("name", OpenApiString),
            _field("in", OpenApiString),
            _field("description", OpenApiString),
            _field("required", OpenApiBoolean, False),
            _field("deprecated", OpenApiBoolean, False),
            _field("allowEmptyValue", OpenApiBoolean, False),

            # Parameter serialization:
            _field("style", OpenApiString),
            _field("explode", OpenApiBoolean, True),
            _field("allowReserved", OpenApiBoolean, False),
            _union(
                _field("schema", SchemaObject),
                _field("content", OpenApiMap.of(MediaTypeObject)),
            ),
            _union(
                _field("example", OpenApiAny),
                _field("examples", OpenApiMap.of(ExampleObject)),
            ),
        )

    def _init_defaults(self, field_defaults):
        param_in = self['in']

        # HACK: add this for providers which leave 'required' implicit.
        #       This is against the spec, but it's not uncommon...
        if param_in == 'path':
            field_defaults['required'] = OpenApiBoolean(True)

        # Default value for style is contingent on the 'in' field:
        if self['style'] is None:
            field_defaults['style'] = OpenApiString({
                'query': 'form',
                'path': 'simple',
                'header': 'simple',
                'cookie': 'form',
            }.get(param_in))

        # Default value for explode is true if style is form; false, otherwise:
        if self['explode'] is None:
            field_defaults['explode'] = OpenApiBoolean(
                {'form': True}.get(self['style'], False))

    @required('name')
    @required('in')
    @in_range('in', ['path', 'query', 'header', 'cookie'])
    @in_range('style',
        ['matrix', 'label', 'form', 'simple', 'spaceDelimited', 'pipeDelimited',
         'deepObject'])
    def _validate(self):
        """
        Compliant with 3.0.3, save for Style Values.

        Todo:
            - `Style Values <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#style-values>`_
        """
        param_in = self['in']
        if param_in == 'path':
            require_value(self, 'required', True)

        # If "content" is defined, there can only be a single entry in the map:
        if self['content'] is not None and len(self['content']) != 1:
            raise InvalidFieldValueException(
                self, 'content', "Length must be 1")


class RequestBodyObject(OpenApiBaseObject):
    """
    .. seealso:: `RequestBodyObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#requestBodyObject>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("description", OpenApiString),
            _field("content", OpenApiMap.of(MediaTypeObject)),
            _field("required", OpenApiBoolean, False),
        )

    @required('content')
    def _validate(self):
        """Validation is 3.0.3 compliant"""
        pass


class MediaTypeObject(OpenApiBaseObject):
    """
    .. seealso:: `MediaTypeObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#mediaTypeObject>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("schema", SchemaObject),
            _union(
                _field("example", OpenApiAny),
                _field("examples", OpenApiMap.of(ExampleObject)),
            ),
            _field("encoding", OpenApiMap.of(EncodingObject)),
        )

    def _validate(self):
        """
        Todo:
            - Keys in encoding must map to parameters in schema.
            - Encoding SHALL only apply when the media type is ``multipart``
              or ``application/x-www-form-url-encoded``
        """
        pass


class EncodingObject(OpenApiBaseObject):
    @classmethod
    def _obj_spec(cls):
        return (
            _field("contentType", OpenApiString),
            _field("headers", OpenApiMap.of(HeaderObject)),
            _field("style", OpenApiString),
            _field("explode", OpenApiBoolean, False),
            _field(
                "allowReserved", OpenApiBoolean, False),
        )

    def _validate(self):
        """
        Todo: validation
        """
        pass



class ResponsesObject(OpenApiMap):
    """
    .. seealso:: `ResponsesObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#responsesObject>`_
    """

    def __init__(self, data, doc_path):
        super().__init__(data, doc_path, ResponseObject)

    def _validate(self):
        """
        Todo:
            - validate keys in map
        """
        pass


class ResponseObject(OpenApiBaseObject):
    """
    .. seealso:: `ResponseObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#responseObject>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("description", OpenApiString),
            _field("headers", OpenApiMap.of(HeaderObject)),
            _field("content", OpenApiMap.of(MediaTypeObject)),
            _field("links", OpenApiMap.of(LinkObject)),
        )

    @required('description')
    def _validate(self):
        """Validation is 3.0.3 compliant"""
        pass


class CallbackObject(OpenApiMap):
    """
    .. seealso:: `CallbackObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#callbackObject>`_

    Todo:
        - Expression-language parsing.
    """

    def __init__(self, data, doc_path):
        super().__init__(data, doc_path, PathItemObject)


class ExampleObject(OpenApiBaseObject):
    """
    .. seealso:: `ExternalDocumentationObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#externalDocumentationObject>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("summary", OpenApiString),
            _field("description", OpenApiString),
            _union(
                _field("value", OpenApiAny),
                _field("externalValue", OpenApiString),
            ),
        )


class LinkObject(OpenApiBaseObject):
    """
    .. seealso:: `LinkObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#linkObject>`_

    Todo:
        - [{in}].{name} parameter key parsing
    """
    @classmethod
    def _obj_spec(self):
        return (
            _union(
                _field("operationRef", OpenApiString),
                _field("operationId", OpenApiString),
            ),
            _field("parameters", OpenApiMap.of(OpenApiAny)),
            _field("requestBody", OpenApiAny),
            _field("description", OpenApiString),
            _field("server", ServerObject),
        )


class HeaderObject(ParameterObject):
    """
    .. seealso:: `HeaderObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#headerObject>`_
    """

    def _validate(self):
        """
        Todo:
            - Same as Parameter object, but 'name' and 'in' MUST not be defined.
        """



class TagObject(OpenApiBaseObject):
    """
    .. seealso:: `TagObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#tag-object>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("name", OpenApiString),
            _field("description", OpenApiString),
            _field("externalDocs", ExternalDocumentationObject),
        )

    @required('name')
    def _validate(self):
        """Validation is 3.0.3 compliant"""
        pass


class SchemaObject(OpenApiBaseObject):
    """
    .. seealso::
     - `SchemaObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#schemaObject>`_
     - `Properties <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#properties>`_
     - `Fixed-fields-20 <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#fixed-fields-20>`_
     - https://json-schema.org/
     - https://tools.ietf.org/html/draft-wright-json-schema-00
     - https://tools.ietf.org/html/draft-wright-json-schema-validation-00
    """
    @classmethod
    def _obj_spec(cls):
        return (
            # Validation Keywords:
            _field("title", OpenApiString),
            _field("multipleOf", OpenApiInteger),  # >1
            _field("maximum", OpenApiNumber),
            _field("exclusiveMaximum", OpenApiBoolean),
            _field("minimum", OpenApiNumber),
            _field("exclusiveMinimum", OpenApiBoolean),
            _field("maxLength", OpenApiInteger),  # >=0
            _field("minLength", OpenApiInteger),  # >=0
            _field("pattern", OpenApiString),
            _field("maxItems", OpenApiInteger),  # >=0
            _field("minItems", OpenApiInteger),  # >=0
            _field("uniqueItems", OpenApiBoolean),
            _field("maxProperties", OpenApiInteger),  # >=0
            _field("minProperties", OpenApiInteger),  # >=0
            _field("required", OpenApiList.of(OpenApiString)),
            _field("enum", OpenApiList.of(OpenApiAny)),

            # OpenApi variations:
            _field("type", OpenApiString),
            _union(
                _field("allOf", OpenApiList.of(cls)),
                _field("oneOf", OpenApiList.of(cls)),
                _field("anyOf", OpenApiList.of(cls)),
                _field("not", OpenApiList.of(cls)),
            ),
            _union(
                _field("items", cls),
                _field("properties", OpenApiMap.of(cls)),
            ),
            _field("additionalProperties",
                   OpenApiAny),  # boolean or Schema
            _field("description", OpenApiString),
            _field("format", OpenApiString),
            _field("default", OpenApiAny),  # TODO: validation

            # Optional Fields:
            _field("nullable", OpenApiBoolean, False),
            _field("discriminator", DiscriminatorObject),
            _field("readOnly", OpenApiBoolean, False),
            _field("writeOnly", OpenApiBoolean, False),
            _field("xml", XMLObject),
            _field("externalDocs", ExternalDocumentationObject),
            _field("example", OpenApiAny),
            _field("deprecated", OpenApiBoolean, False),
        )

    def _validate(self):
        # Only readOnly or writeOnly can be true:
        if self['readOnly']:
            require_value(self, 'writeOnly', False)
        elif self['writeOnly']:
            require_value(self, 'readOnly', False)

        # Discriminator only valid for oneOf, anyOf, allOf:
        if self['discriminator']:
            if (('oneOf' not in self) and ('anyOf' not in self)
                    and ('allOf' not in self)):
                raise MalformedDocumentException(
                    self, 'discriminator',
                    'only valid when using "oneOf", "anyOf", or "allOf"')


class DiscriminatorObject(OpenApiBaseObject):
    """
    .. seealso:: `DiscriminatorObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#discriminatorObject>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("propertyName", OpenApiString),
            _field("mapping", OpenApiMap.of(OpenApiString)),
        )

    @required('propertyName')
    def _validate(self):
        """
        Todo:
            - Ensure match between field and one of defined responses.
        """
        pass


class XMLObject(OpenApiBaseObject):
    """
    .. seealso:: `XmlObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#xmlObject>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("name", OpenApiString),
            _field("namespace", OpenApiString),
            _field("prefix", OpenApiString),
            _field("nullable", OpenApiBoolean, False),
            _field("attribute", OpenApiBoolean, False),
            _field("wrapped", OpenApiBoolean, False),
        )

    @is_url('namespace', require_abs=True)
    def _validate(self):
        pass


class SecuritySchemeObject(OpenApiBaseObject):
    """
    .. seealso:: `SecuritySchemeObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#securitySchemeObject>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("type", OpenApiString),
            _field("description", OpenApiString),
            _field("name", OpenApiString),
            _field("in", OpenApiString),
            _field("scheme", OpenApiString),
            _field("bearerFormat", OpenApiString),
            _field("flows", OAuthFlowsObject),
            _field("openIdConnectUrl", OpenApiString),
        )

    @required('type')
    @is_url('openIdConnectUrl')
    @in_range('type', ["apiKey", "http", "oauth2", "bearer", "openIdConnect"])
    def _validate(self):
        """Validation is 3.0.3 compliant"""
        auth_type = self['type']

        if auth_type == 'apiKey':
            require(self, 'name')
            require(self, 'in')
        elif auth_type == 'http':
            # NOTE: IANA registered auth schemes can be found here:
            # https://www.iana.org/assignments/http-authschemes/http-authschemes.xhtml
            require(self, 'scheme')
        elif auth_type == 'auth2':
            require(self, 'flows')
        elif auth_type == 'openIdConnect':
            require(self, 'openIdConnectUrl')
        elif auth_type in ('http', 'bearer'):
            require(self, 'bearerFormat')


class OAuthFlowsObject(OpenApiBaseObject):
    """
    .. seealso:: `OauthFlows-object <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#oauth-flows-object>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("implicit", OAuthFlowObject),
            _field("password", OAuthFlowObject),
            _field("clientCredentials", OAuthFlowObject),
            _field("authorizationCode", OAuthFlowObject),
        )


class OAuthFlowObject(OpenApiBaseObject):
    """
    .. seealso:: `OauthFlow-object <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#oauth-flow-object>`_

    TODO: context-dependent validation
    """
    @classmethod
    def _obj_spec(cls):
        return (
            # TODO: implicit/authorizationCode, (REQUIRE)
            _field("authorizationUrl", OpenApiString),
            # TODO: password/clientCredentials/authorizationCode, (REQUIRE)
            _field("tokenUrl", OpenApiString),
            _field("refreshUrl", OpenApiString),
            _field("scopes", OpenApiMap.of(OpenApiString)),
        )

    @required('scopes')
    def _validate(self):
        pass


class SecurityRequirementObject(OpenApiMap):
    """
    .. seealso:: `SecurityRequirementObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#securityRequirementObject>`_
    """

    def __init__(self, data, doc_path):
        super().__init__(data, doc_path, OpenApiString)
        return

    def _validate(self):
        """
        Todo:
            - Validate scopes for oauth2 or openIdConnect
            - Validate empty otherwise
        """
        pass


class OpenApiObject(OpenApiBaseObject):
    """
    .. seealso:: `OpenApiObject <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#openapi-object>`_
    """
    @classmethod
    def _obj_spec(cls):
        return (
            _field("openapi", OpenApiString),
            _field("info", InfoObject),
            _field("servers", OpenApiList.of(ServerObject)),
            _field("paths", PathsObject),
            _field("components", ComponentsObject),
            _field("security", OpenApiList.of(
                SecurityRequirementObject)),
            _field("tags", OpenApiList.of(TagObject)),
            _field("externalDocs", ExternalDocumentationObject),
        )

    def __init__(self, doc_src, doc_path="#", resolve_refs=False):
        data = load_yaml(doc_src)
        self.__resolve_refs = resolve_refs
        self.__obj_by_path = {}
        super().__init__(data, doc_path)
        return

    @property
    def _obj_by_path(self):
        """
        List nested document elements by path.
        """
        return self.__obj_by_path

    def _post_init(self):
        """
        Populate objects by path and optionally resolve references.
        """
        self.accept(self.__add_obj_by_path)

        if self.__resolve_refs:
            self.accept(self.__resolve_ref)
        return

    @required('openapi')
    @required('info')
    @required('paths')
    def _validate(self):
        """TODO"""
        pass

    def __add_obj_by_path(self, child):
        """
        Visitor method to add child objects to the path index.
        """
        if child is self or child is None:
            return

        self.__obj_by_path[child.doc_path] = child
        return

    def __resolve_ref(self, child):
        """
        Visitor method used to resolve reference, when indicated.
        """
        if child is self or child is None:
            return

        # TODO: tidy
        if isinstance(child, ReferenceObject):
            target = self.__obj_by_path.get(child.ref)
            child._resolve_ref(target)
        return


def openapi_by_path(doc):
    return doc._obj_by_path


# EOF
