from argparse import ArgumentParser
import json

def main(): # hi
    test = False

    # num_found = {selector_name : selector_count}
    num_found = {}
    # get local json file as command line args
    parser = ArgumentParser(description='get json for input')
    parser.add_argument('input', type=str, help="json file")

    args = parser.parse_args()

    # load the json file into a dictionary views
    with open(args.input, 'r') as f:
        views = json.load(f)

    # get selector from user
    print('class e.g. StackView, classNames e.g. .container, identifier e.g. #videoMode')
    selector = input('Enter selector: ')
    while selector: # enter nothing to exit

        # get attribute type from prefix
        if selector[0] == '.':
            attrib = 'classNames'
            selector = selector[1:]
        elif selector[0] == '#':
            attrib = 'identifier'
            selector = selector[1:]
        else:
            attrib = 'class'

        # for implementing the bonus questions i was thinking of splitting
        # the input and running the first token to generate a list of views or roots,
        # num_found = {compound_selector_name : [list of json views]}
        # then i could call the 2nd selector on each one of those json views to
        # see if it is a child

        # store the number found
        num_found = {selector : 0}
        search_json(views, selector, attrib, num_found, test)
        print('{} found {} views'.format(selector, num_found[selector]))
        # select another item
        selector = input('Enter selector: ')

    # begin test
    # not sure if you wanted an assertion statement
    # or just the number printed on the screen as above
    test = True
    attrib = 'class'
    num_found['Input'] = 0
    search_json(views, 'Input', attrib, num_found, test)

    assert num_found['Input'] == 26, 'Input should return 26 items. returned {}'.format(num_found['Input'])
    print('All Done..\n')


# print the children starting from the root in json format, if in test, do not
# print anything
def print_children(root, test):
    if test:
        return
    print('{}\n'.format(json.dumps(root, indent=4)))


# recursively iterate through the dictionary, if search term is found, print
# children using the term's container as the root, and track the count for
# each earch term in a table
def search_json(json_obj, term, attrib, num_found, test):
    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            # check if a className is in a list of ClassNames
            # if so, print the view
            if k == attrib and isinstance(v, list):
                for item in v:
                    if item == term:
                        num_found[term] +=1
                        print_children(json_obj, test)
            # if the value matches the search term, print view
            elif v == term and k == attrib:
                num_found[term] +=1
                print_children(json_obj, test)
            else:
                search_json(v, term, attrib, num_found, test)
    elif isinstance(json_obj, list):
        for value in json_obj:
            search_json(value, term, attrib, num_found, test)

if __name__ == '__main__':
    main()
