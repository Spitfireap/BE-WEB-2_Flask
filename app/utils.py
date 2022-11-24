import hashlib
import random 
import string


def _generateur_sel():
    sel = ''
    for i in range(0, 64):
        sel += random.choice(string.ascii_letters+string.digits)
    return str(sel)


def hash(password):
    """Pour créer un mdp."""
    sel = _generateur_sel()
    # On encode le pre_hash pour etre sur qu'il y est que du ASCII (si accents et autre dans le mdp...)
    pre_hash = str.encode(password + sel)

    mdp_hash = hashlib.md5(pre_hash).hexdigest()  # On hash le mdp avec le sel
    return mdp_hash, sel  # Pour la DB


def check_hash(password, sel):
    """Pour verifier un mdp."""
    pre_hash = str.encode(password+sel)

    mdp_hash = hashlib.md5(pre_hash).hexdigest()  # On hash le mdp avec le sel
    return mdp_hash  # Pour la DB
