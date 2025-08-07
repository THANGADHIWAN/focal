"""
Quality events models for the Sample Management API
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum, Float
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.utils.constants import InvestigationPhase, DeviationSeverity, DeviationStatus, CapaActionType, CapaStatus, CapaTaskStatus


class OOS(Base):
    __tablename__ = "oos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_id = Column(Integer, ForeignKey("sample.id"))
    test_id = Column(Integer, ForeignKey("test.id"))
    instrument_id = Column(Integer, ForeignKey("instrument.id"))
    test_method_id = Column(Integer, ForeignKey("test_method.id"))
    result_value = Column(Float)
    specification_limit_low = Column(Float)
    specification_limit_high = Column(Float)
    unit = Column(String(50))
    result_status = Column(String(50))
    analyst_name = Column(String(100))
    test_location = Column(String(100))
    oos_detected_at = Column(DateTime)
    oos_flag_auto = Column(Boolean, nullable=False, default=False)
    oos_flag_manual = Column(Boolean, nullable=False, default=False)
    notification_timestamp = Column(DateTime)
    oos_reference_number = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    sample = relationship("Sample", backref="oos_events")
    test = relationship("Test", backref="oos_events")
    instrument = relationship("Instrument", backref="oos_events")
    test_method = relationship("TestMethod", backref="oos_events")
    oos_investigations = relationship("OOSInvestigation", back_populates="oos", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<OOS {self.id}: {self.oos_reference_number}>"


class OOSInvestigation(Base):
    __tablename__ = "oos_investigation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    oos_id = Column(Integer, ForeignKey("oos.id"), nullable=False)
    phase = Column(Enum(InvestigationPhase), nullable=False, default=InvestigationPhase.PHASE1_LAB)
    investigation_start = Column(DateTime)
    investigator_name = Column(String(100))
    raw_data_reviewed_at = Column(DateTime)
    retest_initiated_at = Column(DateTime)
    retest_result = Column(Float)
    is_retest_passed = Column(Boolean)
    analyst_interview_at = Column(DateTime)
    root_cause_method = Column(String(100))
    root_cause_description = Column(Text)
    conclusion = Column(String(255))
    qa_reviewer_name = Column(String(100))
    investigation_complete_at = Column(DateTime)
    documents_uploaded_at = Column(DateTime)
    capa_required = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    oos = relationship("OOS", back_populates="oos_investigations")

    def __repr__(self):
        return f"<OOSInvestigation {self.id}: {self.phase}>"


class Deviation(Base):
    __tablename__ = "deviation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reported_by = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"))
    reported_at = Column(DateTime)
    department = Column(String(100))
    deviation_type = Column(String(100))
    severity = Column(Enum(DeviationSeverity), nullable=False)
    deviation_status = Column(Enum(DeviationStatus), nullable=False, default=DeviationStatus.OPEN)
    gmp_impact = Column(Boolean)
    process_impacted = Column(String(100))
    related_sop_id = Column(Integer, ForeignKey("test_procedure.id"))
    description = Column(Text)
    root_cause_method = Column(String(100))
    root_cause_description = Column(Text)
    investigation_comments = Column(Text)
    deviation_reference_number = Column(String(100))
    linked_oos_id = Column(Integer, ForeignKey("oos.id"))
    approved_by = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"))
    approval_timestamp = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    reporter = relationship("Users", foreign_keys=[reported_by], backref="reported_deviations")
    approver = relationship("Users", foreign_keys=[approved_by], backref="approved_deviations")
    related_sop = relationship("TestProcedure", backref="deviations")
    linked_oos = relationship("OOS", backref="linked_deviations")
    capas = relationship("CAPA", back_populates="linked_deviation")

    def __repr__(self):
        return f"<Deviation {self.id}: {self.deviation_reference_number}>"


class CAPA(Base):
    __tablename__ = "capa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    initiated_by = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"))
    initiation_timestamp = Column(DateTime)
    department = Column(String(100))
    root_cause_method = Column(String(100))
    root_cause_description = Column(Text)
    action_type = Column(Enum(CapaActionType), nullable=False, default=CapaActionType.BOTH)
    corrective_action_plan = Column(Text)
    preventive_action_plan = Column(Text)
    action_owner = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"))
    action_due_date = Column(DateTime)
    task_completed_at = Column(DateTime)
    voe_performed_by = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"))
    voe_outcome = Column(Text)
    approval_by = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"))
    approval_timestamp = Column(DateTime)
    linked_deviation_id = Column(Integer, ForeignKey("deviation.id"))
    linked_oos_id = Column(Integer, ForeignKey("oos.id"))
    capa_status = Column(Enum(CapaStatus), nullable=False, default=CapaStatus.OPEN)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    initiator = relationship("Users", foreign_keys=[initiated_by], backref="initiated_capas")
    action_owner_rel = relationship("Users", foreign_keys=[action_owner], backref="owned_capas")
    voe_performer = relationship("Users", foreign_keys=[voe_performed_by], backref="voe_capas")
    approver = relationship("Users", foreign_keys=[approval_by], backref="approved_capas")
    linked_deviation = relationship("Deviation", back_populates="capas")
    linked_oos = relationship("OOS", backref="linked_capas")
    capa_actions = relationship("CAPAAction", back_populates="capa", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CAPA {self.id}: {self.capa_status}>"


class CAPAAction(Base):
    __tablename__ = "capa_action"

    id = Column(Integer, primary_key=True, autoincrement=True)
    capa_id = Column(Integer, ForeignKey("capa.id"), nullable=False)
    task_description = Column(Text)
    assigned_to = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"))
    due_date = Column(DateTime)
    completed_at = Column(DateTime)
    task_status = Column(Enum(CapaTaskStatus), nullable=False, default=CapaTaskStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)

    capa = relationship("CAPA", back_populates="capa_actions")
    assigned_user = relationship("Users", backref="assigned_capa_actions")

    def __repr__(self):
        return f"<CAPAAction {self.id}: {self.task_status}>" 