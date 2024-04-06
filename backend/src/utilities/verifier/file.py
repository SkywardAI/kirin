# FileVerifier Used for file operation validation.
class FileVerifier:
    # is file_name available
    def is_file_available(self, name: str | None) -> bool:
        if name:
            return False
        return True


def get_file_verifier() -> FileVerifier:
    return FileVerifier()


file_verifier: FileVerifier = get_file_verifier()
