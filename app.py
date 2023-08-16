import streamlit as st
# import artfornormies.functions as art
import plotly.graph_objects as go
### if issue with plotly Figure().write_image() function: pip install -U kaleido
from io import BytesIO


# #colorschemes for MARKERS
# hk_redgreen = [[0, 'rgb(168,16,42)' ],
#                  [0.5, 'rgb(255,255,255)'],
#                 [1, "rgb(16,168,142)"]]

# hk_redblue = [[0, 'rgb(168,16,42)' ],
#                  [0.5, 'rgb(255,255,255)'],
#                 [1, "rgb(16,118,168)"]]

# hk_bluered = [[0, "rgb(16,118,168)" ],
# #                  [0.5, 'rgb(255,255,255)'],
#                 [1, 'rgb(168,16,42)']]

# hk_greenred = [[0, "rgb(16,168,142)" ],
#                  [0.5, 'rgb(255,255,255)'],
#                 [1, 'rgb(168,16,42)']]

#individual colors
hk_red = 'rgb(168,16,42)' #A8102A
hk_green = 'rgb(16,168,142)' #7bedda
hk_blue = 'rgb(16,118,168)'

hk_red_light = "rgb(240, 125, 144)"
hk_green_light = "rgb(123, 237, 218)"
hk_blue_light = "rgb(126, 203, 242)"

# hk_redgreen_l = [[0, hk_red_light ],
#                  [0.5, 'rgb(255,255,255)'],
#                 [1, hk_green_light]]

# off_white='#e4dfce'
# off_white="white"
# off_black='#242424'

# sand_823 = "#adab8b"
# salmon_823 = "#ad8b8f"
# blue_823 = "#8b93ad"

# triad_1 = [sand_823, salmon_823, blue_823]

data_font='Futura'
title_font='Futura'

# fig_width=1000
# fig_height=1200

anno_text_default = "Source: <i>https://github.com/jon-tk-chan</i><br><i>Instagram: @artfornormies</i>"

#NEWLINED FUNCTION - for inserting breaks into text labels for graphs
def newlined(input_string, max_line_len=12):
    """Return a string with <br> added when one line reaches max_line_len in place of the next space
    
    Use for individual plotly labels (especially with scatter)
    """
#     input_split = input_string.split()
#     print(input_split)
    
    curr_line_len = 0
    out_str = ""
    for i, char in enumerate(input_string):
        curr_line_len += 1
        if char == " " and curr_line_len >= max_line_len:
            out_str += "<br>"
            curr_line_len = 0
        else: 
            out_str += char
        
    return out_str


def create_venn_2(venn_labels=["LEFT", "RIGHT","MID"], fill_venn=False, 
                  left_color=hk_blue, right_color=hk_red, label_charlen=10,
                  main_title="VENN_TITLE",anno_text=anno_text_default,night_mode=False,
                  fig_width=1000, fig_height=1200, label_size=28):
    """Returns a Plotly Figure of a 2-circle venn diagram with labels (left, right, middle itersection)
    
    Optional settings:
    
    text_size: int
    left_color = predefined color (str)
    right_color = predefined color (str)
    night_mode: boolean
    """
    title_size = 32 #not referenced?
    # label_size = 30
    anno_size = 14
    if not night_mode:
        outline_color="black"
        font_color="black"
        bg_color="white"
        opacity_val = 0.25
        line_color="black"
       
    else:
        outline_color="white"
        font_color="white"
        bg_color="black"
        opacity_val = 0.7
        line_color="white"
        
    if not fill_venn:
        left_fill = None
        right_fill = None
        line_weight=7
    else:
        left_fill = left_color
        right_fill = right_color
        line_weight=3
    data_dict = {
        "x": [1,2,3],
        "y": [1,1,1],
            "text": [newlined(venn_labels[0], label_charlen), newlined(venn_labels[2],label_charlen),newlined(venn_labels[1],label_charlen)]
    }
#     print(data_dict['text'])
    fig = go.Figure()

    ### ADD VENN DIAGRAMS
    fig.add_trace(go.Scatter(
        x = data_dict["x"],
        y = data_dict["y"],
        text = data_dict['text'],
        mode="text",
        textfont=dict(
            color=font_color,
            size=label_size,
            family=data_font,
        )
    ))
    fig.add_shape(type="circle",
        line_color=line_color, line_width=line_weight,
                  fillcolor=left_fill,
        x0=0.5, y0=0, x1=2.5, y1=2,
                  layer='below'
    )
    fig.add_shape(type="circle",
        line_color=line_color, line_width=line_weight,
                  fillcolor=right_fill,
        x0=1.5, y0=0, x1=3.5, y1=2,
                  layer='below'
    )

    fig.update_shapes(opacity=opacity_val, xref="x", yref="y")

    # Update axes properties
    fig.update_xaxes(showticklabels=False,showgrid=False,zeroline=False,
    )

    fig.update_yaxes(showticklabels=False,showgrid=False,zeroline=False,
    )

    fig.update_layout(
        title=main_title,
        font=dict(family=data_font, size=title_size,color=font_color),
        plot_bgcolor=bg_color, paper_bgcolor=bg_color,
        height=fig_height, #use width for height so that image is not stretched
        width=fig_width,
        margin=dict(l=20, r=20, b=100),
    )

    #add annotation
    fig.add_annotation(
        text = anno_text, showarrow=False,
        x = 0.04, y = -0.1125, #controls how far from axes 
        xref='paper', yref='paper' , xanchor='left', yanchor='bottom',
        font=dict(size=anno_size), align="left",
    )

    return fig








###### DEFAULT HEADER #######
st.header("Artfornormies - dashboard test")
st.markdown("""
    Test making a deployable dashboard that allows you to write venn diagram things 
""")
            
###### INPUTS IN FORM #####       
col1, col2 = st.columns(2)  
with col1:
    with st.form('Form1'):        
        left_text = st.text_input("left text", value='LEFT')
        right_text= st.text_input("right side text", "RIGHT")
        center_text = st.text_input("center text", value='CENTER')
        title_text = st.text_input("title text:", value="MAIN TITLE")
        # max_text_width = st.slider(label='select max length of text line (char):', 
        #                         min_value=0, max_value=50, value = 10)
        # image_dims = st.select_slider('select edge length and width (px): ', 
        #                             options=[500, 600, 700, 800, 900, 1000, 1100, 1200],
        #                             value=700)
        # lab_size = st.slider('select label font size:',
        #                     min_value=8, max_value=50,value=28)
        submitted = st.form_submit_button('Submit')

with col2:
    with st.form('Form2'):        
        # left_text = st.text_input("left text", value='LEFT')
        # right_text= st.text_input("right side text", "RIGHT")
        # center_text = st.text_input("center text", value='CENTER')
        max_text_width = st.slider(label='select max length of text line (char):', 
                                min_value=0, max_value=50, value = 10)
        image_dims = st.select_slider('select edge length and width (px): ', 
                                    options=[500, 600, 700, 800, 900, 1000, 1100, 1200],
                                    value=700)
        lab_size = st.slider('select label font size:',
                            min_value=8, max_value=50,value=28)
        st.markdown('###### \n ####') #used to align spacing for 
        submitted = st.form_submit_button('Submit')



# st.write(submitted)
# st.write(f"LEFT TEXT: {left_text}")
# st.write(f"RIGHT TEXT: {right_text}")
# st.write(f"CENTER TEXT: {center_text}")




fig = create_venn_2( venn_labels=[left_text, right_text, center_text], 
                        night_mode=True, fill_venn=True, 
                        label_charlen=max_text_width,
                        main_title=title_text, fig_width=image_dims, fig_height=image_dims,
                        label_size=lab_size)
#pass any Plotly updates as you would with any Plotly figure - add to artfornormies functions later?
# fig.update_layout(width=image_dims, height=image_dims)


buf = BytesIO()
fig.write_image(buf, format="JPEG")
byte_im = buf.getvalue()
btn = st.download_button(
      label="Download Image",
      data=byte_im,
      file_name="imagename.png",
      mime="image/jpeg",
      )

st.plotly_chart(fig)