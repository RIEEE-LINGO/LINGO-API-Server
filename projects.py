from flask import abort
from config import db
from lingo.models import Project, project_schema, projects_schema


def get_all():
    projects = Project.query.all()
    return projects_schema.dump(projects)


def get(project_id):
    project = Project.query.where(Project.id == project_id).one_or_none()

    if project is not None:
        return project_schema.dump(project)
    else:
        abort(
            404, f"Project with id {project_id} not found"
        )


def create(project):
    new_project = project_schema.load(project, session=db.session)
    db.session.add(new_project)
    db.session.commit()
    return project_schema.dump(new_project), 201


def update(project_id, project):
    existing_project = Project.query.where(Project.id == project_id).one_or_none()
    if existing_project:
        update_project = project_schema.load(project, session=db.session)
        existing_project.project_name = update_project.project_name
        existing_project.project_owner = update_project.project_owner
        existing_project.is_active = update_project.is_active
        db.session.merge(existing_project)
        db.session.commit()
        return project_schema.dump(existing_project), 201
    else:
        abort(
            404,
            f"Project with id {project_id} not found"
        )
