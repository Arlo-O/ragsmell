import ast

from ragsmell.astutils import call_name, endswith_any, import_aliases


def test_call_name_and_boundary():
    node = ast.parse("client.chat.completions.create('x')").body[0].value
    assert call_name(node) == "client.chat.completions.create"
    assert endswith_any(call_name(node), ["create"])
    assert not endswith_any("recreate", ["create"])


def test_import_aliases():
    tree = ast.parse("import openai as oa\nfrom langchain import ChatOpenAI as Chat")
    assert import_aliases(tree) == {"oa": "openai", "Chat": "langchain.ChatOpenAI"}
