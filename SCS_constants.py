import pandas as pd
import networkx as nx
import numpy as np
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Set, Tuple, Union
import streamlit as st
import matplotlib.pyplot as plt


index_values = ["Blue, IO, US(D1)", "Blue, IO, EU(D2)", 
                "Blue, WP, US(D3)", "Blue, WP, EU(D4)", 
                "Brown, IO, US (D5)", "Brown, IO, EU (D6)", 
                "Brown, WP, US (D7)", "Brown, WP, EU (D8)",
                "No ship (D9)"]
US_objectives = ['Legitimacy US', "Reduce burden US", 'Deter China', 'Maintain economic relations China', 'Maintain military relations China', 'Freedom of Seas', 'Deter Russia', 'Defeat Russia']

df_us = pd.DataFrame(index=index_values, columns= US_objectives,  data= 0 )
df_us.loc['Blue, IO, US(D1)', :] = [0, -1, 0, -1, -1, 1, -1, -1]
df_us.loc['Blue, IO, EU(D2)', :] = [1, 0, 0, -1, -1, 1, -1, -1]

df_us.loc['Blue, WP, US(D3)', :] = [0, -1, 1, -1, -1, 1, -1, -1]
df_us.loc['Blue, WP, EU(D4)', :] = [1, -1, 0, -1, -1, 1, -1, -1]

df_us.loc['Brown, IO, US (D5)', :] = [0, -1, 0, 0, 0, 0, -1, -1]
df_us.loc['Brown, IO, EU (D6)', :] = [0, 0, 0, 0, 0, 0, -1, -1]

df_us.loc['Brown, WP, US (D7)', :] = [0, -1, -1, 0, 0, 0, -1, -1]
df_us.loc['Brown, WP, EU (D8)', :] = [0, -1, -1, 0, 0, 0, -1, -1]

df_us.loc['No ship (D9)', :] = [0, 0, -1, 0, 0, 0, 0, 0]


DF_US = df_us

# add the objectives for China and Europe

# make Paul van hooft rank these in order to create a utility matrix
# play the game and visualize it on a dashboard
# Dataframe from the EU perspective
EU_objectives = ['Deter China/reassure EastAsia', 'Relations US', 'Freedom of Seas', 'Relations ASEAN', 'Relations China', 'Deter/defeat Russia']
df_eu = pd.DataFrame(index=index_values, columns= EU_objectives,  data= 0 )
df_eu.loc['Blue, IO, US(D1)', :] = [0, 0, 0, -1, -1, 0]
df_eu.loc['Blue, IO, EU(D2)', :] = [1, 1, 1, 0, 0, -1]

df_eu.loc['Blue, WP, US(D3)', :] = [1, 0, 0, -1, -1, 0]
df_eu.loc['Blue, WP, EU(D4)', :] = [1, 0, 1, -1, -1, -1]

df_eu.loc['Brown, IO, US (D5)', :] = [1, 0, 0, 0, -1, 0]
df_eu.loc['Brown, IO, EU (D6)', :] = [1, 1, 0, 1, 0, 0]

df_eu.loc['Brown, WP, US (D7)', :] = [0, 0, 0, 0, -1, 0]
df_eu.loc['Brown, WP, EU (D8)', :] = [1, 0, 0, 0, 0, -1]

df_eu.loc['No ship (D9)', :] = [-1, -1, -1, 1, -1, 1]
DF_EU = df_eu


China_objectives = ['Maintain relations with US: avoid military confrontation', 'Maintain relations with US: avoid economic confrontation', 'Avoid US aid to TW', 'Limis US freedom of maneuver in WP', 'Consolidate CN power in WP', 'Maintain relations with ASEAN', 'Maintain relations with EUR']
df_cn= pd.DataFrame(index=index_values, columns= China_objectives,  data= 0 )
df_cn.loc['Blue, IO, US(D1)', :] = [0, 0, 0, -1, -1, 0, 0]
df_cn.loc['Blue, IO, EU(D2)', :] = [1, 1, 1, 0, 0, -1, 0]

df_cn.loc['Blue, WP, US(D3)', :] = [1, 0, 0, -1, -1, 0, 0]
df_cn.loc['Blue, WP, EU(D4)', :] = [1, 0, 1, -1, -1, -1, 0]

df_cn.loc['Brown, IO, US (D5)', :] = [1, 0, 0, 0, -1, 0, 0]
df_cn.loc['Brown, IO, EU (D6)', :] = [1, 1, 0, 1, 0, 0, 0]

df_cn.loc['Brown, WP, US (D7)', :] = [0, 0, 0, 0, -1, 0, 0]
df_cn.loc['Brown, WP, EU (D8)', :] = [1, 0, 0, 0, 0, -1, 0]

df_cn.loc['No ship (D9)', :] = [-1, -1, -1, 1, -1, 1, 0]
DF_CN = df_cn

def draw_macid(macid):
    """
    Draw the CBN, CID, or MACID using NetworkX and Matplotlib.
    """
    layout = nx.kamada_kawai_layout(macid)

    plt.figure()
    nx.draw_networkx(macid, pos=layout, node_size=800, arrowsize=20)

    label_dict = {node: macid._get_label(node) for node in macid.nodes}
    pos_higher = {}
    for k, v in layout.items():
        if v[1] > 0:
            pos_higher[k] = (v[0] - 0.1, v[1] - 0.2)
        else:
            pos_higher[k] = (v[0] - 0.1, v[1] + 0.2)

    nx.draw_networkx_labels(macid, pos_higher, label_dict)

    for node in macid.nodes:
        nx.draw_networkx(
            macid.to_directed().subgraph([node]),
            pos=layout,
            node_size=800,
            arrowsize=20,
            node_color=macid._get_color(node),
            node_shape=macid._get_shape(node),
        )

    st.pyplot(plt)



# def draw_macid(
#         self,
#         node_color: Callable[[str], Union[str, np.ndarray]] = None,
#         node_shape: Callable[[str], str] = None,
#         node_label: Callable[[str], str] = None,
#         layout: Optional[Callable[[Any], Dict[Any, Any]]] = None,
#     ) -> None:
#         """
#         Draw the CBN, CID, or MACID.
#         """
#         color = node_color if node_color else self._get_color
#         shape = node_shape if node_shape else self._get_shape
#         label = node_label if node_label else self._get_label
#         layout = layout(self) if layout else nx.kamada_kawai_layout(self)  # type: ignore
#         label_dict = {node: label(node) for node in self.nodes}
#         pos_higher = {}
#         for k, v in layout.items():  # type: ignore
#             if v[1] > 0:
#                 pos_higher[k] = (v[0] - 0.1, v[1] - 0.2)
#             else:
#                 pos_higher[k] = (v[0] - 0.1, v[1] + 0.2)
#         nx.draw_networkx(self, pos=layout, node_size=800, arrowsize=20)
#         nx.draw_networkx_labels(self, pos_higher, label_dict)
#         for node in self.nodes:
#             nx.draw_networkx(
#                 self.to_directed().subgraph([node]),
#                 pos=layout,
#                 node_size=800,
#                 arrowsize=20,
#                 node_color=color(node),
#                 node_shape=shape(node),
#             )
#         return 