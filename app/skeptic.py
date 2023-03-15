from datetime import datetime

class Skeptic:

    def generate_interventions(self, data):

        print('===================================')
        prompts = dict()

        skeptic = data['Skeptic']
        aif = data['AIF']
        nodes = aif['nodes']
        locutions = [x for x in nodes if x['type'] == 'L' and not x['text'].startswith('Anon:')]
        self.order_locutions(locutions)
        for row in skeptic['questions']:
            nodeID = row['nodeID']
            aif_node = self.find_aif_node(aif, nodeID)

            related_locs = self.getRelatedLocutions(aif, aif_node)

            #from these locutions find the most recent one.
            latest_locution = self.most_recent_locution(related_locs)
            if latest_locution != None:
                #add a tuple of the latest locution ID and the prompt to be given.
                nodeID = latest_locution['nodeID']
                prompt_tuple = (row['question'], row['type'])
                if nodeID in prompts:
                    prompts[nodeID].append(prompt_tuple)
                else:
                    prompts[nodeID] = []
                    prompts[nodeID].append(prompt_tuple)
        
        print(prompts)
        return prompts, locutions



    def order_locutions(self, locs):
        n = len(locs)
        swapped = False
        for i in range(n-1):
            for j in range(0, n-i-1):
                date_j = datetime.strptime(locs[j]['timestamp'], '%Y-%m-%d %H:%M:%S')
                date_jplus1 = datetime.strptime(locs[j+1]['timestamp'], '%Y-%m-%d %H:%M:%S')
                if date_j > date_jplus1:
                    locs[j], locs[j+1] = locs[j+1], locs[j]
                    swapped = True
            
            if not swapped:
                print('No swaps required!')
                return
    

    """
    This method takes as input a nodeID and returns the complete node/object
    from the aif json object.
    """
    def find_aif_node(self, aif, nodeID):
        for row in aif['nodes']:
            if(row['nodeID'] == nodeID):
                return row


    """
    This method takes as input an AIF node and returns the related L-nodes. 
    """
    def getRelatedLocutions(self, aif, node):
        locutions = []
        
        #If the node is an S-node, we identify the incoming/outgoing I-nodes and then move to their connecting locutions.
        if node['type'] == "RA" or node['type'] == "CA" or node['type'] == "MA" or node['type'] == "TA" or node['type'] == "PA":
            nodeID = node['nodeID']

            for edge in aif['edges']:
                if edge['fromID'] == nodeID: #search for outgoing edges
                    toID = edge['toID']
                    nodeTo = self.find_aif_node(aif, toID)
                    if nodeTo['type'] == "I":
                        loc = self.get_Lnode(aif, nodeTo['nodeID'])
                        locutions.append(loc)
                
                elif edge['toID'] == nodeID: #search for incoming edges
                    fromID = edge['fromID']
                    nodeFrom = self.find_aif_node(aif, fromID)
                    if nodeFrom['type'] == "I":
                        loc = self.get_Lnode(aif, nodeFrom['nodeID'])
                        locutions.append(loc)
                        
        # if the node is an I-node, we get directly the connected locution.             
        elif node['type'] == "I":
            loc = self.get_Lnode(aif, node['nodeID'])
            locutions.append(loc)
            
        return locutions


    """
    This method returns the most recent locution from an array of locutions, based 
    on the way they are arranged in the ordered_locutions array.
    """
    def most_recent_locution(self, locutions):
        latest_loc = locutions[0]
        latest_date = datetime.strptime(latest_loc['timestamp'], '%Y-%m-%d %H:%M:%S')
        for loc in locutions:
            loc_date = datetime.strptime(loc['timestamp'], '%Y-%m-%d %H:%M:%S')
            if(loc_date > latest_date) :
                latest_loc = loc
                latest_date = loc_date
                    
        return latest_loc


    """
    This method takes as input an I-node and returns the connected L-node
    """
    def get_Lnode(self, aif, inodeID):
        #get the edges that result to the iNodeID
        edges_targetting_I = [edge for edge in aif['edges'] if edge['toID'] == inodeID]
        
        for e in edges_targetting_I:
            s_nodeID = e['fromID']
            s_node = self.find_aif_node(aif, s_nodeID)
            # find the incoming YAs
            if(s_node['type'] == "YA"):
                yaID  = s_node['nodeID']
                edges_targetting_YA = [edge for edge in aif['edges'] if edge['toID'] == yaID]
                lnodeID = edges_targetting_YA[0]['fromID']
                lnode = self.find_aif_node(aif, lnodeID)
                return lnode

