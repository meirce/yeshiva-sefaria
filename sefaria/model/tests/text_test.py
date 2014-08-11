from sefaria.model import *
import sefaria.model.dependencies
import regex as re
from copy import deepcopy


def test_index_methods():
    assert text.Index().load_by_query({"title": "Rashi"}).is_commentary()
    assert not text.Index().load_by_query({"title": "Exodus"}).is_commentary()


def test_index_delete():
    #Simple Text

    #Commentator


    pass


def test_index_name_change():

    #Simple Text
    old = u"Exodus"
    new = u"Movement of Ja People"

    for cnt in dep_counts(new).values():
        assert cnt == 0

    old_counts = dep_counts(old)

    index = text.Index().load_by_query({"title": old})
    old_index = deepcopy(index)
    new_in_alt = new in index.titleVariants
    index.title = new
    index.save()
    assert old_counts == dep_counts(new)

    index.title = old
    if not new_in_alt:
        index.titleVariants.remove(new)
    index.save()
    assert old_index == index
    assert old_counts == dep_counts(old)
    for cnt in dep_counts(new).values():
        assert cnt == 0

    #Commentator


def dep_counts(name):
    ref_patterns = {
        'alone': r'^{} \d'.format(re.escape(name)),
        'commentor': r'{} on'.format(re.escape(name)),
        'commentee': r'on {} \d'.format(re.escape(name))
    }

    commentee_title_pattern = r'on {}'.format(re.escape(name))

    ret = {
        'version title exact match': text.VersionSet({"title": name}).count(),
        'version title match commentor': text.VersionSet({"title": {"$regex": ref_patterns["commentor"]}}).count(),
        'version title match commentee': text.VersionSet({"title": {"$regex": commentee_title_pattern}}).count(),
        'history title exact match': history.HistorySet({"title": name}).count(),
        'history title match commentor': history.HistorySet({"title": {"$regex": ref_patterns["commentor"]}}).count(),
        'history title match commentee': history.HistorySet({"title": {"$regex": commentee_title_pattern}}).count(),
    }

    for pname, pattern in ref_patterns.items():
        ret.update({
            'note match ' + pname: note.NoteSet({"ref": {"$regex": pattern}}).count(),
            'link match ' + pname: link.LinkSet({"refs": {"$regex": pattern}}).count(),
            'history refs match ' + pname: history.HistorySet({"ref": {"$regex": pattern}}).count(),
            'history new refs match ' + pname: history.HistorySet({"new.refs": {"$regex": pattern}}).count()
        })

    return ret