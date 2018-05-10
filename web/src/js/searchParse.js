/**
 * Created by MoNeY_Pro on 2016/3/10.
 */

function camelize(str) {
    return str.replace(/(?:^\w|[A-Z]|\b\w)/g, function(letter, index) {
        return index == 0 ? letter.toLowerCase() : letter.toUpperCase();
    }).replace(/\s+/g, '').replace(/\+/g, '');
}

var getQueryString = function (name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return (r[2]);
    return "";
};


$.getJSON("./assets/searchResults/"+camelize(getQueryString("name"))+".json", function(json) {
    //console.log(json); // this will show the info it in firebug console
    if (json.About) {
        document.getElementById("title").innerHTML += json.About.results.irrelevant[0].Name;
        document.getElementById("Name").innerHTML = json.About.results.irrelevant[0].Name;
        document.getElementById("About").innerHTML = json.About.results.irrelevant[0].About;
        document.getElementById("Homepage").innerHTML = json.About.results.irrelevant[0].Homepage;
        document.getElementById("Linkedin").innerHTML = json.About.results.irrelevant[0].LinkedIn;
        document.getElementById("Collaborators").innerHTML = parseList(json.Collaborators);
        document.getElementById("School").innerHTML = parseList(json.School);
        document.getElementById("Publication").innerHTML = parseCategory(json.Publication);
    }
    else {
        document.getElementById("title").innerHTML += "Paper search";
        document.getElementById("Name").innerHTML = getQueryString("name").replace(/\+/g, ' ');
        document.getElementById("About").innerHTML = "<p> You searched for a paper. It is at <a href = 'https://www.era.lib.ed.ac.uk/handle/1842/14236'>https://www.era.lib.ed.ac.uk/handle/1842/14236</a>.</p> Similar results are listed below.";
        document.getElementById("Publication").innerHTML = parseList(json.Related);
    }

});
function parseCategory(json){
    var result = "";
    for (var i in json.results.irrelevant) {
        //console.log();
        for (var j in json.schema) {
            var category = json.schema[j].name;
            var value = json.results.irrelevant[i][category];
            if (typeof(value)=="object"){
                //Later
            }
            else if (typeof(value)=="string"){
                if(value!=""){
                    //console.log(result);
                    if (category == "Title")
                        result += "<h3>"+value+"</h3>";
                    else
                        result += "<p>"+value+"</p>";
                }
            }
        }
    }
    return result;
}

function parseList(json){
    var result = "";
    for (var i in json) {
        //console.log();
            var value = json[i];
            if (typeof(value)=="object"){
                //Later
            }
            else if (typeof(value)=="string"){
                if(value!=""){
                    result += "<p>"+value+"</p>";
                }
            }

    }
    return result;
}