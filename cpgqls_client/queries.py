
def import_code_query(path, project_name=None, language=None):
    if not path:
        raise Exception('An importCode query requires a project path')
    if project_name and language:
        fmt_str = u"""importCode(inputPath=\"%s\", projectName=\"%s\",
language=\"%s\")"""
        return fmt_str % (path, project_name, language)
    if project_name and (language is None):
        fmt_str = u"""importCode(inputPath=\"%s\", projectName=\"%s\")"""
        return fmt_str % (path, project_name)
    return u"importCode(\"%s\")" % (path)


def open_query(project_name):
    return f"open(\"{project_name}\")"


def close_query(project_name):
    return f"close(\"{project_name}\")"


def delete_query(project_name):
    return f"delete(\"{project_name}\")"


def help_query():
    return f"help"


def workspace_query():
    return "workspace"


def project_query():
    return "project"
