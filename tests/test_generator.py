from types import SimpleNamespace
from unittest.mock import Mock, patch

from afripay.generator import generate_scaffold


def test_generate_scaffold_returns_mocked_code_for_mpesa_fastapi() -> None:
    mocked_code = "# generated scaffold\nMPESA_MARKER = True"
    mock_response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(content=mocked_code),
            )
        ]
    )
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("afripay.generator.OpenAI", return_value=mock_client):
        result = generate_scaffold("mpesa", "fastapi")

    assert result
    assert "MPESA_MARKER" in result

    create_call = mock_client.chat.completions.create
    create_call.assert_called_once()
    _, kwargs = create_call.call_args
    assert kwargs["model"] == "gpt-4o"

    prompt = kwargs["messages"][1]["content"]
    assert "ip_allowlist+resultcode" in prompt
