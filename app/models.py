from __future__ import annotations
import datetime
import uuid
from typing import List
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Date, DateTime, Table
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
from .database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(String, unique=True)

    users = relationship("User", back_populates="users")

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(UUID, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="user")
    employee = relationship("Employee", uselist=False, back_populates="employee")
    manager = relationship("Employee", back_populates="manager")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"))
    avatar_url = Column(String)
    phone = Column(String)
    job_position = Column(String)
    department = Column(String)
    manager_id = Column(UUID, ForeignKey("users.id"))
    work_location = Column(String)
    summary = Column(Text)
    # created_date = Column(DateTime, default=datetime.datetime.utcnow)

    experiences = relationship("Experience", back_populates="experiences")
    educations = relationship("Education", back_populates="educations")
    licenses = relationship("License", back_populates="licenses")


class Experience(Base):
    __tablename__ = "experiences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID, ForeignKey("employees.id"))
    company_name = Column(String)
    position = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)

    employee = relationship("Employee", back_populates="experience")


project_programming_language = Table(
    "project_programming_language",
    Base.metadata,
    Column("experience_project_id", ForeignKey("experience_projects.id"), primary_key=True),
    Column("programming_language_id", ForeignKey("programming_languages.id"), primary_key=True),
)

project_framework = Table(
    "project_framework",
    Base.metadata,
    Column("experience_project_id", ForeignKey("experience_projects.id"), primary_key=True),
    Column("framework_id", ForeignKey("frameworks.id"), primary_key=True),
)

project_server = Table(
    "project_server",
    Base.metadata,
    Column("experience_project_id", ForeignKey("experience_projects.id"), primary_key=True),
    Column("server_id", ForeignKey("servers.id"), primary_key=True),
)

class ExperienceProject(Base):
    __tablename__ = "experience_projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    experience_id = Column(UUID, ForeignKey("experiences.id"))
    name = Column(String)
    overview = Column(Text)
    team_size = Column(Integer)
    website = Column(String)
    position = Column(String)
    responsibility = Column(Text)
    # other = Column(Text)

    programming_languages: Mapped[List[ProgrammingLanguage]] = relationship(secondary=project_programming_language, back_populates="projects")
    frameworks: Mapped[List[Framework]] = relationship(secondary=project_framework, back_populates="projects")
    servers: Mapped[List[Server]] = relationship(secondary=project_server, back_populates="projects")


class ProgrammingLanguage(Base):
    __tablename__ = "programming_languages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    language = Column(String, nullable=False)

    projects: Mapped[List[ExperienceProject]] = relationship(secondary=project_programming_language, back_populates="programming_languages")


class Framework(Base):
    __tablename__ = "frameworks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    framework = Column(String, nullable=False)

    projects: Mapped[List[ExperienceProject]] = relationship(secondary=project_framework, back_populates="frameworks")


class Server(Base):
    __tablename__ = "servers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    server = Column(String, nullable=False)

    projects: Mapped[List[ExperienceProject]] = relationship(secondary=project_server, back_populates="servers")

class Education(Base):
    __tablename__ = "educations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID, ForeignKey("employees.id"))
    institute_name = Column(String)
    degree = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)

    employee = relationship("Employee", back_populates="education")


class License(Base):
    __tablename__ = "licences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID, ForeignKey("employees.id"))
    license_name = Column(String)
    issuing_organization = Column(String)
    credential_id = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    credential_url = Column(String)

    employee = relationship("Employee", back_populates="licence")
