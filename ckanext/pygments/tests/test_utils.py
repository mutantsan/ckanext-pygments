from types import SimpleNamespace

from ckanext.pygments import utils


def test_get_file_resource_data(monkeypatch):
    file_info = {
        "location": "resources/example.py",
        "storage": "resources",
    }

    class Storage:
        def stream(self, data):
            assert data.location == file_info["location"]
            yield b"print('hello')\n"
            yield b"ignored"

    files_api = SimpleNamespace(
        get_storage=lambda _name: Storage(),
        FileData=SimpleNamespace(
            from_dict=lambda data: SimpleNamespace(location=data["location"]),
        ),
    )
    monkeypatch.setattr(utils, "_get_files_api", lambda: files_api)
    monkeypatch.setattr(
        utils.tk,
        "get_action",
        lambda _name: lambda _context, data: file_info if data["id"] == "file-id" else None,
    )

    resource = SimpleNamespace(
        id="resource-id",
        url="https://ckan.example/file/download/file-id",
    )

    assert utils.get_file_resource_data(resource, 5) == "print"
