import string
import random

import connexion


def rand_string(length):
    chars = string.ascii_letters + string.punctuation
    return "".join(random.choice(chars) for x in range(20))


class Resolver(connexion.resolver.RestyResolver):
    def resolve_operation_id_using_rest_semantics(self, operation):
        """
        Resolves the operationId using REST semantics
        :type operation: connexion.operations.AbstractOperation
        """

        # Split the path into components delimited by '/'
        path_components = [c for c in operation.path.split("/") if len(c)]

        def is_var(component):
            """True if the path component is a var. eg, '{id}'"""
            return (component[0] == "{") and (component[-1] == "}")

        resource_name = ".".join([c for c in path_components if not is_var(c)]).replace(
            "-", "_"
        )
        if resource_name[-1] == "s":
            resource_name = resource_name[:-1]

        def get_controller_name():
            x_router_controller = operation.router_controller

            name = self.default_module_name

            if x_router_controller:
                name = x_router_controller

            elif resource_name:
                d = self.default_module_name
                r = resource_name
                name = f"{d}.controller.{r}"
                print("+_+_+_+", d, r, name)

            return name

        def get_function_name():
            method = operation.method

            is_collection_endpoint = (
                method.lower() == "get"
                and len(resource_name)
                and not is_var(path_components[-1])
            )

            return (
                self.collection_endpoint_name
                if is_collection_endpoint
                else method.lower()
            )

        print(f"{get_controller_name()}.{get_function_name()}")
        return f"{get_controller_name()}.{get_function_name()}"
