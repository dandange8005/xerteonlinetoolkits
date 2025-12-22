# Getting started with XERTE XOT Theme

The DigED XOT Theme provides great flexibility when it comes to customising the look and feel of your own project. Follow this guide to see how you can change some of the CSS properties to create a unique project of your own.

!!! note
    🔔 You don't need any prior knowledge of CSS but you should be comfortable with code.

## Video Tutorial
[https://youtu.be/Gro2jOtdVFE](https://youtu.be/Gro2jOtdVFE)

## Changing the theme colour
Colours can be changed quite easily by altering the [custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/--*) within the project.

To change the main theme colour:

1. Copy the code below

    ```css
    :where(html) {
    /*Accent colour*//*Main accent colour controls the title page shade and the page header background */
    --clr-accent: hsl(217, 59%, 20%);
        --clr-h: 217;
        --clr-s: 59%;
        --clr-l: 20%;
    }
    ```

2. Open you XOT project
3. Paste the code into the Styles field. This would allow you to overwrite the default CSS properties.
    
    ![https://i.imgur.com/hTUxuVP.png](https://i.imgur.com/hTUxuVP.png)
    
4. Choose a colour of your choice and make a note of the HSL value. In this example, I used [Google Colour Picker](https://g.co/kgs/m4765a) to pick a colour that I liked. Note down the HSL value `246, 90%, 33%` .
    
    <aside>
    🔔 **note**
    Feel free to use any colour tools you like but make sure you note down the HSL value of the colour.
    
    </aside>
    
5. Go back to your Xerte project and apply the new values to the Styles
    
    ```css
    :where(html) {
    /*Accent colour*//*Main accent colour controls the title page shade and the page header background */
    --clr-accent: hsl(246, 90%, 33%);
    --clr-h: 246;
    --clr-s: 90%;
    --clr-l: 33%;
    }
    ```
    
6. Click `Play` button to preview the changes. You should be able to see the new colour been applied to the title page as well as the header area.
    
    ![https://i.imgur.com/CiTLQEk.png](https://i.imgur.com/CiTLQEk.png)
    

## Updating the Title Page

### Remove the rounded shade effect

1. Click on the **Title Page** and find the **Styles** field
    
    ![https://i.imgur.com/axNXz7h.png](https://i.imgur.com/axNXz7h.png)
    
2. Locate the following code:

    ```css
    /*pseudo element for gradient overlay, with fallback colour options*/#x_mainHolder::before {
        content: ' ';
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        opacity: 0.95;
        background: linear-gradient(105deg, var(--clr-accent) 55%, transparent 55%);
        background: radial-gradient(ellipse 75% 150% at bottom right, transparent 0%, transparent 75%, var(--clr-accent) 75%);
    }
    ```

3. Comment out the last line of code which gives the shade a rounded effect
    
    ```css
    #x_mainHolder::before {
        content: ' ';
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        opacity: 0.95;
        background: linear-gradient(105deg, var(--clr-accent) 55%, transparent 55%);
    /*background: radial-gradient(ellipse 75% 150% at bottom right, transparent 0%, transparent 75%, var(--clr-accent) 75%);*/
    }
    ```
    
4. You may also change the degree value within this property `background: linear-gradient(105deg, var(--clr-accent) 55%, transparent 55%);` to change the angle of the shade.

### Changing the background image

Once again, with the Title Page selected, you can change the background image by replacing the image in the Image field of the Background property.

![https://i.imgur.com/QZLzMzG.png](https://i.imgur.com/QZLzMzG.png)