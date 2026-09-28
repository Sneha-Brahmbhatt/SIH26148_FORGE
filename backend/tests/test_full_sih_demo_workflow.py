"""
FORGE Mandatory End-to-End SIH Demo Test Workflow
Tests complete pipeline:
Script → Lexer → Parser → AST → Semantic Validation → Policy Check → Controlled Execution → Evidence → Hashes → Provenance → Timeline → Findings → Chain of Custody → Report → Audit Trail
"""

import pytest
from language.lexer import Lexer
from language.parser import Parser
from language.semantic import SemanticValidator
from language.policy import PolicyEngine
from language.runtime import Interpreter
from app.api.routes import DEMO_FULL_ANALYSIS_SCRIPT, DEMO_POLICY_BLOCKED_SCRIPT

def test_full_sih_demo_workflow():
    # Step 1: Lexer Tokenization
    lexer = Lexer(DEMO_FULL_ANALYSIS_SCRIPT)
    tokens = lexer.tokenize()
    assert len(tokens) > 20
    assert tokens[0].value == "CASE"

    # Step 2: Parser & AST Construction
    parser = Parser(tokens)
    ast = parser.parse()
    assert ast.node_type == "ProgramNode"
    assert len(ast.statements) >= 5

    # Step 3: Semantic Validation
    validator = SemanticValidator()
    diagnostics = validator.validate(ast)
    errors = [d for d in diagnostics if d["level"] == "ERROR"]
    assert len(errors) == 0

    # Step 4: Capability & Policy Engine Check
    policy_engine = PolicyEngine("standard-read-only-v1")
    policy_res = policy_engine.evaluate(ast)
    assert policy_res["decision"] == "APPROVED"
    assert "HOST_READ" in policy_res["invoked_capabilities"]
    assert len(policy_res["denied_capabilities"]) == 0

    # Step 5: Controlled Runtime Execution
    interpreter = Interpreter("standard-read-only-v1")
    result = interpreter.execute(
        program=ast,
        script_id="SCR-SIH-001",
        script_version="1.0.0",
        script_source=DEMO_FULL_ANALYSIS_SCRIPT,
        case_id="CASE-001",
        analyst_id="investigator@org.example"
    )

    # Step 6: Verify Execution Result Integrity
    assert result["status"] == "COMPLETED"
    assert result["policy_decision"] == "APPROVED"
    assert len(result["evidence"]) >= 5
    assert len(result["timeline"]) >= 5
    assert len(result["findings"]) >= 3
    assert len(result["reports_created"]) >= 1
    assert result["provenance"] is not None

    # Step 7: Verify Hash-Chained Audit Log Integrity
    audit_summary = result["audit_summary"]
    assert audit_summary["chain_valid"] is True
    assert audit_summary["total_records"] >= 8

def test_policy_blocked_demo_workflow():
    # Lex & Parse Blocked Script
    lexer = Lexer(DEMO_POLICY_BLOCKED_SCRIPT)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    # Policy Check must reject
    policy_engine = PolicyEngine("standard-read-only-v1")
    policy_res = policy_engine.evaluate(ast)
    assert policy_res["decision"] == "BLOCKED"
    assert "WRITE_EVIDENCE" in policy_res["denied_capabilities"]
    assert "EXECUTE_PROCESS" in policy_res["denied_capabilities"]

    # Controlled Runtime execution must be prevented before start
    interpreter = Interpreter("standard-read-only-v1")
    result = interpreter.execute(
        program=ast,
        script_id="SCR-BAD-001",
        script_version="1.0.0",
        script_source=DEMO_POLICY_BLOCKED_SCRIPT,
        case_id="CASE-BAD",
        analyst_id="unauthorized@org.example"
    )

    assert result["status"] == "BLOCKED"
    assert result["policy_decision"] == "BLOCKED"
    assert len(result["evidence"]) == 0
    assert len(result["timeline"]) == 0

    # Verify POLICY_DENIED audit log recorded
    audit_logs = result["audit_logs"]
    actions = [a["action"] for a in audit_logs]
    assert "POLICY_DENIED" in actions
