from .. import main

def test_get_playlsit_id():
	assert main.get_playlist_id("www.invalid.link.com/asdf") == None
	assert main.get_playlist_id("https://youtube.com/playlist?lis=PLxCzCOWd7aiGz9donHRrE9I3Mwn6XdP8p") == None
	assert main.get_playlist_id("https://youtube.com/playlist?list=PLZ1QII7yudbc-Ky058TEaOstZHVbT-2hg&si=RYcaiOtldPFJgyRF") == "PLZ1QII7yudbc-Ky058TEaOstZHVbT-2hg"
	assert main.get_playlist_id("https://youtube.com/playlist?list=PLxCzCOWd7aiGz9donHRrE9I3Mwn6XdP8p") == "PLxCzCOWd7aiGz9donHRrE9I3Mwn6XdP8p"

def test_format_duration():
    assert main.format_duration("1:02:03:04") == "1 Days, 02 Hours, 03 Minutes, 04 Seconds"
    assert main.format_duration("12:34:56") == "12 Hours, 34 Minutes, 56 Seconds"
    assert main.format_duration("01:23") == "01 Minutes, 23 Seconds"
    assert main.format_duration("59") == "59 Seconds"
    assert main.format_duration("") == "0 Seconds"


if __name__ == "__main__":
    pytest.main()