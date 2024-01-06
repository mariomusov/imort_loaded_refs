# Author:      Mario Musov | Techincal Animator/Rigger
# Contacts:    https://www.linkedin.com/in/mariomusov/
# Date:        2024-01-06
# Description: Imports loaded reference recursively and deletes their namespaces         

import maya.cmds as cmds

def get_references():
    return cmds.file(query=True, reference=True)

def is_reference_loaded(reference):
    return cmds.referenceQuery(reference, isLoaded=True)
    
def import_reference(reference):
    cmds.file(reference, importReference=True)
    
def get_non_system_namespaces():
    all_namespaces = cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)
    non_system_namespaces = []
    for ns in all_namespaces:
        if ns not in ['UI', 'shared']:
            non_system_namespaces.append(ns)

    return non_system_namespaces
    
def delete_namespaces():
    namespaces = get_non_system_namespaces()
    # Sort them from child to parent as that is the order needed for the delete
    sorted_namespaces = sorted(namespaces, key=lambda ns: ns.count(':'), reverse=True)
    for ns in sorted_namespaces:
        cmds.namespace(removeNamespace=ns, mergeNamespaceWithParent=True)
       
all_refs = get_references()
for ref in all_refs:
    try:
        # Import the refererence only if it is loaded in the scene
        if is_reference_loaded(ref):
            import_reference(ref)
    except RuntimeError:
        pass

    # Check for any new references to import:
    check_refs = get_references()
    for check_ref in check_refs:
        # Add the new reference to the list only if it is loaded
        if is_reference_loaded(check_ref):
            if check_ref not in all_refs:
                all_refs.append(check_ref)

# Delete namespaces when after all references have been imported                
delete_namespaces()


