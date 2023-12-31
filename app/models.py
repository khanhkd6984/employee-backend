from __future__ import annotations
import uuid
from typing import List
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, Table
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
from .database import Base


user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)


class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(String, unique=True, nullable=False)

    users: Mapped[List[User]] = relationship(
        secondary=user_role, back_populates="roles"
    )


# employee_manager = Table(
#     "employee_manager",
#     Base.metadata,
#     Column("employee_id", ForeignKey("employees.id"), primary_key=True),
#     Column("manager_id", ForeignKey("users.id"), primary_key=True),
# )


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    badge_number = Column(String, unique=True, nullable=False)

    # employee = relationship("Employee")

    roles: Mapped[List[Role]] = relationship(
        secondary=user_role, back_populates="users"
    )
    # employees: Mapped[List[Employee]] = relationship(
    #     secondary=employee_manager, back_populates="managers"
    # )


# class Employee(Base):
#     __tablename__ = "employees"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = Column(UUID, ForeignKey("users.id"), unique=True, nullable=False)
#     avatar_url = Column(String)
#     phone = Column(String)
#     job_position = Column(String)
#     department = Column(String)
#     work_location = Column(String)
#     summary = Column(Text)

#     user = relationship("User", overlaps="employee")
#     managers: Mapped[List[User]] = relationship(
#         secondary=employee_manager, back_populates="employees"
#     )


# class Experience(Base):
#     __tablename__ = "experiences"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     employee_id = Column(UUID, ForeignKey("employees.id"))
#     company_name = Column(String)
#     position = Column(String)
#     start_date = Column(Date)
#     end_date = Column(Date)
#     description = Column(Text)

#     employee = relationship("Employee")


# project_programming_language = Table(
#     "project_programming_language",
#     Base.metadata,
#     Column(
#         "experience_project_id", ForeignKey("experience_projects.id"), primary_key=True
#     ),
#     Column(
#         "programming_language_id",
#         ForeignKey("programming_languages.id"),
#         primary_key=True,
#     ),
# )

# project_framework = Table(
#     "project_framework",
#     Base.metadata,
#     Column(
#         "experience_project_id", ForeignKey("experience_projects.id"), primary_key=True
#     ),
#     Column("framework_id", ForeignKey("frameworks.id"), primary_key=True),
# )

# project_server = Table(
#     "project_server",
#     Base.metadata,
#     Column(
#         "experience_project_id", ForeignKey("experience_projects.id"), primary_key=True
#     ),
#     Column("server_id", ForeignKey("servers.id"), primary_key=True),
# )


# class ExperienceProject(Base):
#     __tablename__ = "experience_projects"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     experience_id = Column(UUID, ForeignKey("experiences.id"))
#     name = Column(String)
#     overview = Column(Text)
#     team_size = Column(Integer)
#     website = Column(String)
#     position = Column(String)
#     responsibility = Column(Text)

#     experience = relationship("Experience")
#     programming_languages: Mapped[List[ProgrammingLanguage]] = relationship(
#         secondary=project_programming_language, back_populates="projects"
#     )
#     frameworks: Mapped[List[Framework]] = relationship(
#         secondary=project_framework, back_populates="projects"
#     )
#     servers: Mapped[List[Server]] = relationship(
#         secondary=project_server, back_populates="projects"
#     )


# class ProgrammingLanguage(Base):
#     __tablename__ = "programming_languages"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     language = Column(String, nullable=False)

#     projects: Mapped[List[ExperienceProject]] = relationship(
#         secondary=project_programming_language, back_populates="programming_languages"
#     )


# class Framework(Base):
#     __tablename__ = "frameworks"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     framework = Column(String, nullable=False)

#     projects: Mapped[List[ExperienceProject]] = relationship(
#         secondary=project_framework, back_populates="frameworks"
#     )


# class Server(Base):
#     __tablename__ = "servers"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     server = Column(String, nullable=False)

#     projects: Mapped[List[ExperienceProject]] = relationship(
#         secondary=project_server, back_populates="servers"
#     )


# class Education(Base):
#     __tablename__ = "educations"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     employee_id = Column(UUID, ForeignKey("employees.id"))
#     institute_name = Column(String)
#     degree = Column(String)
#     start_date = Column(Date)
#     end_date = Column(Date)
#     description = Column(Text)

#     employee = relationship("Employee")


# class License(Base):
#     __tablename__ = "licences"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     employee_id = Column(UUID, ForeignKey("employees.id"))
#     license_name = Column(String)
#     issuing_organization = Column(String)
#     credential_id = Column(String)
#     issue_date = Column(Date)
#     expiration_date = Column(Date)
#     credential_url = Column(String)

#     employee = relationship("Employee")
