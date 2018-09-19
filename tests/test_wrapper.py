from pytest import fixture, raises
import vcr

from wrapper import TV
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


@vcr.use_cassette('tests/vcr_cassettes/tv-popular.yml')
def test_tv_popular(tv_keys):
    """Tests an API call to get popular TV shows"""
    response = TV.popular()
    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['results'][0], dict)
    assert set(tv_keys).issubset(response['results'][0].keys())


def test_tv_search_empty(tv_keys):
    """Tests an API call to get popular TV shows"""
    with raises(InvalidInputTMDBError):
        TV.search('')


@vcr.use_cassette('tests/vcr_cassettes/tv-search.yml')
def test_tv_search(tv_keys):
    response = TV.search('The Big bang')
    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['results'][0], dict)
    assert set(tv_keys).issubset(response['results'][0].keys())


@vcr.use_cassette('tests/vcr_cassettes/tv-search.yml')
def test_tv_search_new(tv_keys):
    from wrapper.search import Finder
    finder = Finder('tv')
    response = finder.search('The Big bang')
    assert isinstance(response, dict)
    assert isinstance(response['results'], list)
    assert isinstance(response['results'][0], dict)
    assert set(tv_keys).issubset(response['results'][0].keys())
