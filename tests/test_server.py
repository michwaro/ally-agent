from fastapi.testclient import TestClient

from ally.server import app


def test_healthz_returns_ok() -> None:
    client = TestClient(app)
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_run_stream_returns_sse_events_for_all_agents() -> None:
    client = TestClient(app)
    response = client.post("/api/run-stream", json={"report_text": "test report"})

    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    for agent in ["Intake", "Translator", "Classifier", "RightsMapper", "ReportGenerator", "Pipeline"]:
        assert agent in response.text


def test_upload_report_accepts_txt_file() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/upload-report",
        files={"file": ("report.txt", b"test report", "text/plain")},
    )

    assert response.status_code == 200
    assert response.json()["report_text"]
