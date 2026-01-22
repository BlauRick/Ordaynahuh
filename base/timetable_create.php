<!--I DONT KNOW-->
<?php include 'stylesheet_call.php'?>
<?php  ?>
<style>
    table{width: 90%;}
    table, td,tr{border: 3px yellowgreen solid;}
    .row10{height: 500px;}
    #classes{
    margin: 10px;
    position: fixed;
    top: 20px;
    right: 150px; 
}
</style>

<h1>Órarend tervező </h1> 
<select name="class_id" id="classes">
    <option value="a">dsasadsdsa</option>
</select>
<table>
    <tr>
        <td colspan="2">
            Tanárok
        </td>
        <td colspan="2">
            Órák
        </td>
        <td colspan="5">
            Órarend
        </td>
    </tr>
    <tr>
        <td colspan="2" >
            <div class="row10" id="teachers"><p draggable="true">aaa</p></div>
        </td>
        <td colspan="2" id="orak">
            <div class="row10">ad</div>
        </td>
        <td colspan="5">
            <div class="row10" id="dropbox">a</div>
        </td>
    </tr>
    <tr>
        <td colspan="4">
            Termek
        </td>
        <td id="oraszam">
            Órák száma: <span></span>
        </td>
        <td colspan="4">
            Visszajelzés
        </td>
    </tr>
    <tr>
        <td colspan="4" rowspan="3">
            <div id="room">u8n7</div>
        </td>
        <td >
            Osztály: <span></span>
        </td>
        <td colspan="4" rowspan="3">
            <div id="resp">hhl</div>
        </td>
    </tr>
    <tr>
        <td>
            Nyelv: <span></span>
        </td>
    </tr>
    <tr>
        <td>
            Csoport: <span></span>
        </td>
    </tr>
</table>


<br><button onclick="location.href='index.php'"  id="home_button">home</button>
<button onclick="location.href='profile.php'"  id="user_button">Felhasználó</button>