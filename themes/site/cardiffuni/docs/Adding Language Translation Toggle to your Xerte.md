# Adding Language Translation Toggle to your Xerte Bootstrap Theme Project

## Introduction

This guide will show you how to add a language translation toggle to your Xerte Bootstrap Theme project. The toggle will allow users to switch between English and Welsh language.

## For Project in English

1. Open your Xerte project
2. Go to first page of your project
3. Make sure **Show Advanced Options** is selected, then click on the **New HTML Code...**
4. Give it a title such as "Language Toggle", then uncheck **Show Title**.
    
    ![Untitled](Adding%20Language%20Translation%20Toggle%20to%20your%20Xerte%20B%20fa503186450e417d883cb94f0019e8ef/Untitled.png)
    
5. Add the following code to the **HTML Code** field:
    
    ```html
    <!--HTML markup -->
    <a href="#" id="language-toggle"> <!--Replace the "#" with the actual link URL-->
    	<span class="fav2"> 
    		<i aria-hidden="true" class="fa fa-language language-toggle-icon" title="Language"></i> 
    		<span style="position:absolute; left:-10000px; top:auto; width:1px; height:1px; overflow:hidden;">Language</span> 
    	</span> 
    	<span class="language-toggle-text">Cymraeg</span>	
    </a>
    ```
    
6. Replace `#` with the actual link URL of the English Project, for example:
    
    ```html
    <a href="https://xerte.cardiff.ac.uk/play_18119" id="language-toggle">
    ```
    
7. Add the following code to the **project info** script field:
    
    ```jsx
    setTimeout(function(){
    //	$("#project-info").prependTo("#ultraEssentialssection1");
        $("#language-toggle").prependTo("#overview")
    }, 200);
    
    ```
    
8. Click **Play** to preview the changes. You should be able to see the language toggle on the top right corner of the page.

## For Project in Welsh

Repeat the steps above but update the html markdown to so that it link back to the English project.

```html
<!--HTML markup -->
<a href="#" id="language-toggle"> <!--Replace the "#" with the actual link URL-->
	<span class="fav2"> 
		<i aria-hidden="true" class="fa fa-language language-toggle-icon" title="Language"></i> 
		<span style="position:absolute; left:-10000px; top:auto; width:1px; height:1px; overflow:hidden;">Language</span> 
	</span> 
	<span class="language-toggle-text">English</span>	
</a>
```