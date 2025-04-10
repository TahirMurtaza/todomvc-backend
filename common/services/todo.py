from common.repositories.factory import RepositoryFactory, RepoType
from common.models.todo import Todo
from app.helpers.exceptions import InputValidationError


class TodoService:

    def __init__(self, config):
        self.config = config
        self.repository_factory = RepositoryFactory(config)
        self.todo_repo = self.repository_factory.get_repository(RepoType.TODO)
    
    def save_todo(self, person_id: str, title: str):
        todo = Todo(person_id=person_id, title=title)
        return self.todo_repo.save(todo)
    
    def get_all_todos_by_person_id(self, person_id: str):
        return self.todo_repo.get_many({"person_id": person_id})
    
    def get_todo_by_id(self, entity_id: str) -> Todo:
        return self.todo_repo.get_one({"entity_id": entity_id})
    
    def update_todo(self, entity_id: str, title: str, is_completed: bool) -> Todo:
        todo = self.get_todo_by_id(entity_id)
        if not todo:
            raise InputValidationError("Todo not found")
        todo.title = title
        todo.is_completed = is_completed
        self.todo_repo.save(todo)
        return todo
    
    def get_completed_todos(self, person_id: str = None) -> list[Todo]:
        filters = {"is_completed": True, "active": True}
        if person_id:
            filters["person_id"] = person_id
        return self.todo_repo.get_many(filters)

    def get_active_todos(self, person_id: str = None) -> list[Todo]:
        filters = {"is_completed": False, "active": True}
        if person_id:
            filters["person_id"] = person_id
        return self.todo_repo.get_many(filters)
    
    def activate_all_todos(self, person_id: str) -> None:
        completed_todos = self.get_completed_todos(person_id)
        for todo in completed_todos:
            todo.is_completed = False
            self.todo_repo.save(todo)
    
    def complete_all_todos(self, person_id: str) -> None:
        active_todos = self.get_active_todos(person_id)
        for todo in active_todos:
            todo.is_completed = True
            self.todo_repo.save(todo)
    
    def delete_todo(self, todo_id: str):
        return self.todo_repo.delete({"entity_id": todo_id})

    def delete_completed_todos(self, person_id: str) -> None:
        completed_todos = self.get_completed_todos(person_id)
        for todo in completed_todos:
            self.todo_repo.delete(todo)