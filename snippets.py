import logging
import argparse
# set the log output file and the log level

logging.basicConfig(filename = "snippets.log", level = logging.DEBUG)

def put(name, snippet):
    """
    Store a snippet with an associated name.

    Returns the name and the snippet
    """
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet
    
def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, return '404: Snippet Not Found'.

    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return "404: Snippet Not Found"
    
def append(name, snippet):
    """
    add to an existing snippet

    Returns the name and the snippet added
    """
    logging.error("FIXME: Unimplemented - append({!r}, {!r})".format(name, snippet))
    return name, snippet
    
def rename(old_name,new_name):
    """
    change name of a snippet to new_name
    """
    logging.error("FIXME: Unimplemented - rename({!r}, {!r})".format(old_name,                                                                  new_name))
    return(new_name)
    
def main():
    """main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="store and retrieve snippets of text")
    arguments = parser.parse_args()
    print(arguments)
    
if __name__=="__main__":
    main()
    