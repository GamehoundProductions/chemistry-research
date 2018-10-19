#!/usr/bin/python3
import itertools
import mendeleev #pip3


class Chemistry:

    def __init__(self, minerals):
        '''
            @param minerals: <list of str>. ['Calcium, Ca', 'Iron, Fe', 'Mg'].
                            A list of chemical elements to calculate reactions.
        '''
        self.elements = self.elements_from_list(minerals)


    def elements_from_list(self, minerals):
        '''
            @param minerals: <list of str>. look at __init__ minerals param
        '''
        if not isinstance(minerals, list):
            raise TypeError('Expecting list, but %s was passed!'\
                            % (type(minerals)))

        chemical_elements = []
        for raw_name in minerals:
            raw_name = raw_name.replace(' ', '')
            splitted_name = raw_name.split(',')
            #string name of the chemical element
            element_name = None
            #object element returned by mendeleev.element function
            element_obj = None

            if len(splitted_name) == 2: #'FullName, Abbriviation' format
                element_name = splitted_name[1]
            else:                       #'Full name' or 'Abbriviation'
                element_name = splitted_name[0]

            try:
                element_obj = mendeleev.element(element_name)
            except Exception:
                raise NameError('%s not found in Mendeleev table!' % element_name)


            chemical_elements.append(element_obj)

        return chemical_elements


    def all_permutations(self, element_list=None):
        if element_list is None:
            element_list = self.elements

        result = []
        for i in range(2, len(element_list) + 1):
            combo = list(itertools.combinations(element_list, i))
            result.extend(combo)

        return set(result)
