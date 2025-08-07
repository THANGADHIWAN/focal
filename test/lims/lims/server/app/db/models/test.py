"""
Test models for the Sample Management API
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
from app.utils.constants import TestStatus, ParameterType, SpecificationType, StepResultEnum, ResultStatusEnum
from sqlalchemy.types import Numeric


class TestMethod(Base):
    __tablename__ = "test_method"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    version = Column(String(20))
    description = Column(Text)
    validated = Column(Boolean, nullable=False, default=False)
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    test_parameters = relationship("TestParameter", back_populates="test_method", cascade="all, delete-orphan")
    test_procedures = relationship("TestProcedure", back_populates="test_method", cascade="all, delete-orphan")
    test_masters = relationship("TestMaster", back_populates="test_method", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TestMethod {self.id}: {self.name}>"


class TestParameter(Base):
    __tablename__ = "test_parameter"

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_method_id = Column(Integer, ForeignKey("test_method.id"), nullable=False)
    parameter_name = Column(String(150), nullable=False)
    parameter_type = Column(Enum(ParameterType), nullable=False)
    unit = Column(String(50))
    description = Column(Text)
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    test_method = relationship("TestMethod", back_populates="test_parameters")
    test_specifications = relationship("TestSpecification", back_populates="test_parameter", cascade="all, delete-orphan")
    test_results = relationship("TestResult", back_populates="test_parameter")

    def __repr__(self):
        return f"<TestParameter {self.id}: {self.parameter_name}>"


class TestSpecification(Base):
    __tablename__ = "test_specification"

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_parameter_id = Column(Integer, ForeignKey("test_parameter.id"), nullable=False)
    specification_name = Column(String(150), nullable=False)
    specification_type = Column(Enum(SpecificationType), nullable=False)
    unit = Column(String(50))
    min_value = Column(Numeric(10, 2))
    max_value = Column(Numeric(10, 2))
    description = Column(Text)
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    test_parameter = relationship("TestParameter", back_populates="test_specifications")

    def __repr__(self):
        return f"<TestSpecification {self.id}: {self.specification_name}>"


class TestProcedure(Base):
    __tablename__ = "test_procedure"

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_method_id = Column(Integer, ForeignKey("test_method.id"), nullable=False)
    procedure_name = Column(String(150), nullable=False)
    procedure_description = Column(Text)
    steps_order = Column(Integer, nullable=False, default=1)
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    test_method = relationship("TestMethod", back_populates="test_procedures")
    test_steps = relationship("TestStep", back_populates="test_procedure", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TestProcedure {self.id}: {self.procedure_name}>"


class TestStep(Base):
    __tablename__ = "test_step"

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_procedure_id = Column(Integer, ForeignKey("test_procedure.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    step_description = Column(Text)
    expected_result = Column(Text)
    actual_result = Column(Text)
    remarks = Column(Text)
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    test_procedure = relationship("TestProcedure", back_populates="test_steps")
    test_step_executions = relationship("TestStepExecution", back_populates="test_step", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TestStep {self.id}: {self.step_number}>"


class TestStepExecution(Base):
    __tablename__ = "test_step_execution"

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_step_id = Column(Integer, ForeignKey("test_step.id"), nullable=False)
    executed_by = Column(String(100))
    executed_on = Column(DateTime, default=datetime.utcnow)
    result = Column(Enum(StepResultEnum), nullable=False)
    remarks = Column(Text)

    test_step = relationship("TestStep", back_populates="test_step_executions")

    def __repr__(self):
        return f"<TestStepExecution {self.id}: {self.result}>"


class TestMaster(Base):
    __tablename__ = "test_master"

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_method_id = Column(Integer, ForeignKey("test_method.id"), nullable=False)
    test_name = Column(String(150), nullable=False)
    test_code = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    frequency = Column(String(50))
    active = Column(Boolean, nullable=False, default=True)
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    test_method = relationship("TestMethod", back_populates="test_masters")
    tests = relationship("Test", back_populates="test_master")

    def __repr__(self):
        return f"<TestMaster {self.id}: {self.test_name}>"


class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_id = Column(Integer, ForeignKey("sample.id"))
    aliquot_id = Column(Integer, ForeignKey("aliquot.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    test_master_id = Column(Integer, ForeignKey("test_master.id"), nullable=False)
    analyst_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"))
    instrument_id = Column(Integer, ForeignKey("instrument.id"))
    scheduled_date = Column(DateTime)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(Enum(TestStatus), nullable=False, default=TestStatus.PENDING)
    remarks = Column(Text)

    sample = relationship("Sample", back_populates="tests")
    aliquot = relationship("Aliquot", back_populates="tests")
    product = relationship("Product", back_populates="tests")
    test_master = relationship("TestMaster", back_populates="tests")
    analyst = relationship("Users", backref="assigned_tests")
    instrument = relationship("Instrument", back_populates="tests")
    test_results = relationship("TestResult", back_populates="test", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Test {self.id}: {self.test_master_id}>"


class TestResult(Base):
    __tablename__ = "test_result"

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_id = Column(Integer, ForeignKey("test.id"), nullable=False)
    test_parameter_id = Column(Integer, ForeignKey("test_parameter.id"), nullable=False)
    result_value = Column(String(100))
    unit = Column(String(50))
    specification_limit = Column(String(100))
    result_status = Column(Enum(ResultStatusEnum), nullable=False)
    result_date = Column(DateTime, default=datetime.utcnow)
    remarks = Column(Text)

    test = relationship("Test", back_populates="test_results")
    test_parameter = relationship("TestParameter", back_populates="test_results")

    def __repr__(self):
        return f"<TestResult {self.id}: {self.result_value}>"
