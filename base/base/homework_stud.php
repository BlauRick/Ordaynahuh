<?php include 'header.php'?>


<style>

.container {height: 90%;width: 85.5%;margin-left: 1%!important;}
/* .container{border: 3px purple solid;} */

</style>


<h1>Házi feladat</h1>
<div class="container">

    <div class="row g-2 rowcols-3">

        <div class="col-2" id="border">
            <div class="box-long">
                <p class="h6">Tantárgyak<hr></p>
            </div>
        </div>
        <div class="col-8 g-1">
            <div class="col" id="border">
                <div class="box-small">
                    <p class="h6">Feladatok<hr></p>
                </div>
            </div>
            <div class="row rowcols-2 g-0">
                <div class="col-9" id="border">
                    <div class="box">
                        <p class="h6">Feladat leírás<hr></p>
                    </div>
                </div>
                <div class="col-3" id="border">
                    <div class="box">
                        <p class="h6">Leadás<hr></p>
                    </div>
                </div>
            </div>

        </div>
        <div class="col-2" id="border">
            <div class="box-long">
                <p class="h6">Várható Dolgozatok<hr></p>
            </div>
        </div>
    </div>



</div>



<br><button onclick="location.href='index.php'" id="home_button">home</button>
<button onclick="location.href='profile.php'" id="user_button">Felhasználó</button>