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

        resource_name = ".".join([c for c in path_components if not is_var(c)]).replace("-", "_")
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
                # name = f"{d}.{r}.controller"
                name = f"{d}.controller.{r}"
            return name

        def get_function_name():
            method = operation.method

            is_collection_endpoint = (
                method.lower() == "get" and len(resource_name) and not is_var(path_components[-1])
            )

            return self.collection_endpoint_name if is_collection_endpoint else method.lower()

        # print(f"{get_controller_name()}.{get_function_name()}")
        return f"{get_controller_name()}.{get_function_name()}"

    # TODO: find a better way to resolve this
    def resolve_operation_id(self, operation):
        # TODO: auto resolve /collection/{item}/collection

        special = {
            "/projects/{project_id}/tasks getTasks": "pplabel.api.controller.task.get_by_project",
            "/projects/{project_id}/labels getLabels": "pplabel.api.controller.label.get_by_project",
            "/projects/{project_id}/labels setLabels": "pplabel.api.controller.label.set_by_project",
            "/projects/{project_id}/labels removeLabels": "pplabel.api.controller.label.delete_by_project",
            "/projects/{project_id}/annotations getAnnotations": "pplabel.api.controller.annotation.get_by_project",
            "/projects/{project_id}/tags getTags": "pplabel.api.controller.tag.get_by_project",
            "/projects/{project_id}/progress getProgress": "pplabel.api.controller.task.get_stat_by_project",
            "/projects/{project_id}/split splitDataset": "pplabel.api.controller.project.split_dataset",
            "/projects/{project_id}/export exportDataset": "pplabel.api.controller.project.exportDataset",
            "/tasks/{task_id}/tags getTags": "pplabel.api.controller.tag.get_by_task",
            "/tasks/{task_id}/tags addTag": "pplabel.api.controller.tag.add_to_task",
            "/datas/{data_id}/image getImage": "pplabel.api.controller.data.get_image",
            "/tasks/{task_id}/annotations getAnnotations": "pplabel.api.controller.annotation.get_by_task",
            "/tasks/{task_id}/datas getDatas": "pplabel.api.controller.data.get_by_task",
            "/datas/{data_id}/annotations getAnnotations": "pplabel.api.controller.annotation.get_by_data",
            "/datas/{data_id}/annotations setAnnotations": "pplabel.api.controller.annotation.set_all_by_data",
            "/datas/{data_id}/annotations deleteAnnotations": "pplabel.api.controller.annotation.delete_by_data",
            "/rpc/folders getFolders": "pplabel.api.rpc.file.get_folders",
        }
        opid = None

        if operation.operation_id and operation.operation_id.startswith("pplabel"):
            opid = operation.operation_id

        path = operation.path
        if path[:-1] == "/":
            path = path[:-1]
        idx = f"{path} {operation.operation_id}"
        if idx in special.keys():
            opid = special[idx]
        # print("resolve resolve resolve", operation.operation_id, path, opid)
        if opid:
            router_controller = operation.router_controller
            if router_controller is None:
                return opid
            return f"{router_controller}.{opid}"

        return self.resolve_operation_id_using_rest_semantics(operation)
