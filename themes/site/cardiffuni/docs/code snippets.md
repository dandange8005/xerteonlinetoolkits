## Footer

Below is an example of a footer that can be used in the Xerte themes. This footer includes the LTA logo and the Digital Education Team details. It also includes a list of useful links that can be customised to suit the needs of the project.

```html
<!-- Footer content -->

<div class="flex flex-wrap">
    <div class="flex-300 flow">
        <img alt="LTA logo" height="95" src="https://dandange8005.github.io/CU-Xerte-Themes/Assets/images/LearningTeachingWhite.png" width="300" />
  <p style="text-align: initial;">Developed by the Digital Education Team
    <br />
    Learning and Teaching Academy
    <br />
    Cardiff University
  </p>
    </div>  
    <div class="flex-300">
        <h3>Useful Links</h3>
        <ul>
            <li><a href="https://xerte.cardiff.ac.uk/play_21502#page1">Learning Central Good Practice Guide</a></li>
            <li><a href="https://xerte.cardiff.ac.uk/play_18321#UltraEssentials">Learning Central Essentials</a></li>
            <li><a href="https://xerte.cardiff.ac.uk/play_18204#page1">Ultra Courses Setup Checklist</a></li>
            <li><a href="https://vimeo.com/showcase/cltamicrolearning">Blackboard Ultra Microlearning Library</a></li>
        </ul>
    </div>

</div>
```

## Project Details

Below is an example of a project information component that can be used in the Xerte themes. This component includes the date the project was created, the date it was last updated and the number of views the project has had. This component can be customised to include any other information that is relevant to the project.

```html

<!-- Project information component --><!-- Feel free to include or remove from your project -->
<div id="project-info">
    <p class="info-item"><span class="fav2"><i aria-hidden="true" class="fa fa-calendar  " title="Calendar "></i><span style="position:absolute; left:-10000px; top:auto; width:1px; height:1px; overflow:hidden;">Calendar </span></span>&nbsp;Created:&nbsp;{globalVars.dateCreated}
    </p>
    <p class="info-item"><span class="fav2"><i aria-hidden="true" class="fa fa-rotate-right  " title="Rotate Right "></i><span style="position:absolute; left:-10000px; top:auto; width:1px; height:1px; overflow:hidden;">Rotate Right </span></span>&nbsp;Updated:&nbsp;{globalVars.lastUpdated}
    </p>
    <p class="info-item"><span class="fav2"><i aria-hidden="true" class="fa fa-eye  " title="Eye "></i><span style="position:absolute; left:-10000px; top:auto; width:1px; height:1px; overflow:hidden;">Eye </span></span>&nbsp;Views:&nbsp;{globalVars.numViews}
    </p>
  </div>
  
  <!--script to insert project information and language toggle to the top of the page-->
  <script>
    setTimeout(function(){
      $("#project-info").prependTo("#page1section1");
    }, 200);
  </script>

```