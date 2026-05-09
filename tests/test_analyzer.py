from types import SimpleNamespace
from unittest.mock import Mock, patch

from ally.analyzer import generate_analysis


def test_generate_analysis_returns_mocked_text_for_report() -> None:
    mocked_analysis = "# Analysis\nRIGHTS_MARKER = True"
    mock_response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(content=mocked_analysis),
            )
        ]
    )
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("ally.analyzer.OpenAI", return_value=mock_client):
        result = generate_analysis("test report", "mpesa")

    assert result
    assert "RIGHTS_MARKER" in result

    create_call = mock_client.chat.completions.create
    create_call.assert_called_once()
    _, kwargs = create_call.call_args
    assert kwargs["model"] == "gpt-4o"

    prompt = kwargs["messages"][1]["content"]
    assert "ip_allowlist+resultcode" in prompt
    assert "test report" in prompt
