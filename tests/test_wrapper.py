from pytest import fixture, raises
import vcr

from wrapper import TV, Finder

from wrapper.exceptions import InvalidInputTMDBError


@fixture
def tv_keys():
    return ['id', 'origin_country', 'poster_path', 'name', 'overview',
            'popularity', 'backdrop_path', 'first_air_date', 'vote_count',
            'vote_average']


@vcr.use_cassette('tests/vcr_cassettes/tv-info.yml')
def test_tv_info(tv_keys):
    """Tests an API call to get a TV show's info"""
    tv_instance = TV(1396)
    tv_instance.update()
    assert tv_instance.id == 1396, "The ID should be in the response"
    assert hasattr(tv_instance, 'name')
    assert hasattr(tv_instance, 'first_air_date')
    assert hasattr(tv_instance, 'popularity')


@vcr.use_cassette('tests/vcr_cassettes/tv-popular.yml', record_mode='all')
def test_tv_popular(tv_keys):
    """Tests an API call to get popular TV shows"""
    tv_shows = TV.popular()
    assert isinstance(tv_shows, list)
    assert isinstance(tv_shows[0], TV)

    tv_shows = TV.popular(1)
    assert isinstance(tv_shows, list)
    assert len(tv_shows) == 1
    assert isinstance(tv_shows[0], TV)


def test_tv_search_empty(tv_keys):
    """Tests an API call to get popular TV shows"""
    with raises(InvalidInputTMDBError):
        TV.search('')


@vcr.use_cassette('tests/vcr_cassettes/tv-search.yml')
def test_tv_search(tv_keys):
    shows = TV.search('The Big bang')
    assert isinstance(shows, list)
    assert isinstance(shows[0], TV)


@vcr.use_cassette('tests/vcr_cassettes/tv-search.yml', record_mode='all')
def test_tv_search_finder(tv_keys):
    finder = Finder('tv')
    shows = finder.search('The Big bang')
    assert isinstance(shows, list)
    assert isinstance(shows[0], TV)


@vcr.use_cassette('tests/vcr_cassettes/tv-info.yml', record_mode='all')
def test_creation_tv(tv_keys):
    data = {
        "id": 1396
    }
    tv_instance = TV.create(data)
    tv_instance.update()
    assert tv_instance.id == 1396, "The ID should be in the response"
    assert hasattr(tv_instance, 'name')
    assert hasattr(tv_instance, 'first_air_date')
    assert hasattr(tv_instance, 'popularity')
