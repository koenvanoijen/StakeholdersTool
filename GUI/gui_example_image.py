import customtkinter
import os
from PIL import Image
import wordcloud_semants


class ScrollableCheckBoxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = customtkinter.CTkCheckBox(self, text=item)
        checkbox.select()
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10))
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.positive_words = list()
        self.negative_words = list()
        self.mindmap_path_save = "test_images/mindmap{today}_{num}.png"
        self.mindmap_last_added_path = None
        self.last_added_freq_list = list()

        self.title("image_example.py")
        self.geometry("1400x900")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                                                 size=(26, 26))
        self.mindmap_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "berry.png")), size=(800, 400))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                                       size=(20, 20))

        # pictures for the left side
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                                 size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
                                                 size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Image Example",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Create Mindmap",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Select words",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w",
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Webscraper",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w",
                                                      command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame

        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(2, weight=1)

        # the Mindcloud picture
        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.mindmap_image)
        self.home_frame_large_image_label.grid(row=0, columnspan=5, padx=20, pady=10)

        # positive words description text
        self.text_field_description_positive_words = customtkinter.CTkTextbox(master=self.home_frame, height=75,
                                                                              width=450)
        self.text_field_description_positive_words.grid(row=1, column=0, padx=10, pady=10)
        self.text_field_description_positive_words.insert("0.0",
                                                          'Below you have to add the positive that you want to find the close words of. add the words one by one and press the add button.')
        # positive words
        self.input_text_field_positive_words = customtkinter.CTkEntry(master=self.home_frame,
                                                                      placeholder_text="type semantic word",
                                                                      width=200)
        self.input_text_field_positive_words.grid(row=2, column=0, padx=20, pady=10)

        self.input_text_positive_add_button = customtkinter.CTkButton(self.home_frame,
                                                                      text="add postive word",
                                                                      compound="left",
                                                                      command=self.add_positive_words_event)
        self.input_text_positive_add_button.grid(row=2, column=1, padx=20, pady=10)

        # the outputwords that is on the second column that is just a text field
        self.output_text_positive_field = customtkinter.CTkTextbox(master=self.home_frame, height=75)
        self.output_text_positive_field.grid(row=1, column=2, padx=20, pady=10)

        self.clear_output_field_positive_button = customtkinter.CTkButton(self.home_frame,
                                                                          text="clear output field",
                                                                          compound="top",
                                                                          command=self.clear_output_field_positive_event,
                                                                          )
        self.clear_output_field_positive_button.grid(row=2, column=2, padx=100, pady=10)

        # negative word description text
        self.text_field_description_negative_words = customtkinter.CTkTextbox(master=self.home_frame, height=75,
                                                                              width=450)
        self.text_field_description_negative_words.grid(row=3, column=0, padx=10, pady=10)
        self.text_field_description_negative_words.insert("0.0",
                                                          'Below you have to add the negative words that you want to be excluded from the mindmap. e.g. if you want to know about light have to add feather and heavy as negative words.')
        # negative words input
        self.input_text_field_negative_words = customtkinter.CTkEntry(master=self.home_frame,
                                                                      placeholder_text="type negative semantic word",
                                                                      width=200)
        self.input_text_field_negative_words.grid(row=4, column=0, padx=100, pady=10)
        self.input_text_negative_add_button = customtkinter.CTkButton(self.home_frame,
                                                                      text="add negative words",
                                                                      compound="top",
                                                                      command=self.add_negative_words_event)
        self.input_text_negative_add_button.grid(row=4, column=1, padx=100, pady=10)

        # the outputwords that is on the second column that is just a text field
        self.output_text_negative_field = customtkinter.CTkTextbox(master=self.home_frame, height=75)

        self.output_text_negative_field.grid(row=3, column=2, padx=20, pady=10)

        self.clear_output_field_negative_button = customtkinter.CTkButton(self.home_frame,
                                                                          text="clear output field",
                                                                          compound="top",
                                                                          command=self.clear_output_field_negative_event)
        self.clear_output_field_negative_button.grid(row=4, column=2, padx=100, pady=10)

        # generate mindmap
        self.home_frame_generate_mindmap = customtkinter.CTkButton(self.home_frame,
                                                                   text="Generate Mindmap",
                                                                   command=self.generate_event)
        self.home_frame_generate_mindmap.grid(row=5, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(2, weight=1)

        # the Mindcloud picture

        self.second_frame_large_image_label = customtkinter.CTkLabel(self.second_frame, text="",
                                                                     image=self.mindmap_image)

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            print('hi')
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")

        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")
        self.go_to_second_page()

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")
        self.go_to_third_page()

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def add_positive_words_event(self):
        """
        takes the input from the input_text_field_positive_words and adds it to the list of positive words
        then it clears the input_text_field_positive_words
        """
        self.positive_words.append(self.input_text_field_positive_words.get())
        self.input_text_field_positive_words.delete(0, "end")
        self.output_text_positive_field.insert("end", self.positive_words[-1] + "\n")

    def add_negative_words_event(self):
        """
        takes the input from the input_text_field_negative_words and adds it to the list of negative words
        then it clears the input_text_field_negative_words
        """
        self.negative_words.append(self.input_text_field_negative_words.get())
        self.input_text_field_negative_words.delete(0, "end")
        self.output_text_negative_field.insert("end", self.negative_words[-1] + "\n")

    def clear_output_field_positive_event(self):
        """
        clears the output_text_positive_field
        """
        self.output_text_positive_field.delete("1.0", "end")
        self.positive_words = []

    def clear_output_field_negative_event(self):
        """
        clears the output_text_negative_field
        """
        self.output_text_negative_field.delete("1.0", "end")
        self.negative_words = []

    def generate_event(self):

        """
        this function is invoked when the generate button is pressed
        then it will take the positive and negative words and generate a mindmap
        it uses worldcloud_semantcs.generate_wordcloud(positive_words, negative_words, path_to_save) to generate the wordcloud and saves it to the path_to_save
        """

        self.mindmap_last_added_path, self.last_added_freq_list = wordcloud_semants.generate_word_cloud(
            positive_words=self.positive_words,
            negative_words=self.negative_words,
            path_to_save=self.mindmap_path_save)
        self.mindmap_image = customtkinter.CTkImage(Image.open(self.mindmap_last_added_path), size=(800, 400))
        self.home_frame_large_image_label.configure(image=self.mindmap_image)

    def add_item(self, item):
        checkbox = customtkinter.CTkCheckBox(self, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10))
        self.checkbox_list.append(checkbox)

    def go_to_second_page(self):
        """
        this function is invoked when the "frame_2" button is pressed
        """
        self.mindmap_image = customtkinter.CTkImage(Image.open(self.mindmap_last_added_path), size=(800, 400))
        self.second_frame_large_image_label.grid(row=0, columnspan=5, padx=20, pady=10)
        self.second_frame_large_image_label.configure(image=self.mindmap_image)

        # create scrollable checkbox frame
        self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=self.second_frame,
                                                                 width=500, height=200,
                                                                 label_text="Words included in wordcloud",
                                                                 item_list=self.last_added_freq_list, label_anchor="w")

        self.scrollable_checkbox_frame.grid(row=1, column=0, padx=15, pady=15, sticky="ns")
        self.scrollable_checkbox_frame.configure(width=500)

        self.scrollable_radiobutton_frame = ScrollableCheckBoxFrame(master=self.second_frame, width=500, height=200,
                                                                    item_list=[f"item {i}" for i in range(100)],
                                                                    label_text="ScrollableRadiobuttonFrame")
        self.scrollable_radiobutton_frame.grid(row=1, column=2, padx=15, pady=15, sticky="ns")
        self.scrollable_radiobutton_frame.configure(width=200)

        self.second_frame_update_mindmap_button = customtkinter.CTkButton(self.second_frame, text="Update Mindmap",
                                                                          command=self.update_mindmap_event)

        self.second_frame_update_mindmap_button.grid(row=1, column=1, padx=20, pady=10)

    def go_to_third_page(self):
        """
        this function is invoked when the "frame_3" button is pressed
        """
        self.mindmap_image = customtkinter.CTkImage(Image.open(self.mindmap_last_added_path), size=(800, 400))
        self.second_frame_large_image_label.grid(row=0, columnspan=5, padx=20, pady=10)
        self.second_frame_large_image_label.configure(image=self.mindmap_image)

        # create link_input box for a link to be put in
        self.link_input_text_box = customtkinter.CTkEntry(self.third_frame, width=200)
        self.link_input_text_box.grid(row=0, column=0, padx=20, pady=10)

        # create a button that uses a default working link
        self.third_frame_default_link_button = customtkinter.CTkButton(self.third_frame, text="Default Link")
        # create a text field that shows how the webscraper traverses the web

        # create a pause button that pauses the webscraper

        # create a button that creates the webscrape graph that shows in the bottem half of frame 3 based on the webcraper data
        # create scrollable checkbox frame


    def create_webscraper_object(self, ):
    def create_correct_words_in_scrollable_frame(self, word_feq_list):
        """
        this function creates a list of words that all have the same legth so that they fit nicely in the scrollable frame
        """
        normal_word = "item{:3}: {:30} {:4}"
        word_list = [normal_word.format(index, item, round(score, 3)) for index, (item, score) in
                     enumerate(word_feq_list)]
        [print(len(item)) for item in word_list]
        return word_list

    def update_mindmap_event(self):
        """
        this function is invoked when the "update mindmap" button is pressed on the second frame
        it looks at the checked boxes and takes all the checked boxes in the page
        """
        selected_positive_words = []
        for checkbox in self.scrollable_checkbox_frame.checkbox_list:
            if checkbox.get() == 1:
                selected_positive_words.append([checkbox.cget("text"), True])
            else:
                selected_positive_words.append([checkbox.cget("text"), False])

        print('selected', selected_positive_words)
        self.mindmap_last_added_path, self.last_added_freq_list = wordcloud_semants.generate_word_cloud_from_freq \
            (frequency_list=selected_positive_words, path_to_save=self.mindmap_path_save)
        self.mindmap_image = customtkinter.CTkImage(Image.open(self.mindmap_last_added_path), size=(800, 400))
        self.second_frame_large_image_label.configure(image=self.mindmap_image)
        # self.scrollable_checkbox_frame.destroy()



if __name__ == "__main__":
    app = App()
    app.mainloop()
