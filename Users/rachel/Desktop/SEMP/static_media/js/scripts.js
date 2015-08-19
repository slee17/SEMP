//************************************
//
// Authors: Orlan Davies, Miles O'Connell, Ryan Wilson 
//			Amanda DaSilva
//
// Claremont McKenna College
// Student Technology Assistance Team
// Personnel Management Package
//
//************************************

//************************************
//Variables for start and end time for schedule display
var startDisp = 8;
var endDisp = 26;
var root = ""; // Delete this to "" in order to deploy


// ************************************************************************************************************************************************
// ************************************************************************************************************************************************
// Start Of General Functions
// ************************************************************************************************************************************************
// ************************************************************************************************************************************************

// get the element with the id given
function $() {
	var elements = new Array();
	for (var i = 0; i < arguments.length; i++) {
		var element = arguments[i];
		if (typeof element == 'string')
			element = document.getElementById(element);
		if (arguments.length == 1)
			return element;
		elements.push(element);
	}
	return elements;
}

// hide named element
function hide(id) {
	if (isVisible(id)) {
		$(id).style.display = 'none';
	}
}

function _status(message) { window.status = message; }
// getter, setter for innerHTML
function getInnerHTML(id) { return $(id).innerHTML; }

function setInnerHTML(id,inner) {
	if($(id) != null){
		$(id).innerHTML = inner;
	} 
}

function appendToHTML(id,app) { $(id).innerHTML = $(id).innerHTML + app; }

// yes, example code
function alphanumeric(alphane) {
	var numaric = alphane;
	for(var i=0; i<numaric.length; i++)
		{
		  var alphaa = numaric.charAt(i);
		  var hh = alphaa.charCodeAt(0);
		  if( !( (hh > 47 && hh<59) || (hh > 64 && hh<91) || (hh > 96 && hh<123) ) ) {
			 return false;
		  }
		}
 return true;
}

// returns true iff named element is visible
function isVisible(id) { return $(id).style.display != 'none'; }

// displays element at given loc
function showAt(id,l,t) {
	$(id).style.left = l+5 + "px";
	$(id).style.top = t+5 + "px";
	showBlock(id);
}

// sets display style of element to block
function showBlock(id) {
	if ($(id).style.display != 'block') {
		$(id).style.display = 'block';
	}
}

// shows element in middle of screen.
function showInMiddle(id,wi,he) {
	var H = parseInt(document.body.clientHeight);
	var W = parseInt(document.body.clientWidth);
	var h = (he) ? (H/2 - he/2) : (H/2 - 50);
	var w = (wi) ? (W/2 - wi/2) : (W/2 - 50);
	if(h < he/2)
		h = he/2;
	showAt(id,w,h);
}

function convertToXML(tag, value){
	return "<"+tag+">"+value+"</"+tag+">";
}
// ------------------------------------------------------------------------------------------------------------------------------------------------
// End General Functions
// ------------------------------------------------------------------------------------------------------------------------------------------------





// ************************************************************************************************************************************************
// ************************************************************************************************************************************************
// Start Of Form Validtion Functions
// ************************************************************************************************************************************************
// ************************************************************************************************************************************************
// check that contents of login form are valid.
function loginFormValid() {
	var message = "";
	if (document.loginForm.username.value == "Username") {
		message += "\n- Username";
	}
	if (document.loginForm.password.value == "") {
		message += "\n- Password";
	}
	if (message == "") {
		return true;
	}
	alert("Please correct the following error(s):" + message);
	return false;
}
// ------------------------------------------------------------------------------------------------------------------------------------------------
// End Of Form Validtion Functions
// ------------------------------------------------------------------------------------------------------------------------------------------------






// ************************************************************************************************************************************************
// ************************************************************************************************************************************************
// Start Of Gateway Functions
// ************************************************************************************************************************************************
// ************************************************************************************************************************************************
function gatewayGetAllInformation(){
	if(controlsLocked) {
		return;
	}
	lockControls();
   	getFiles();
	gatewayGetShifts();
	getCatNews();
	getDepNews();
	getSales();
	getPermanentSales();
	adminGetUsers();
	unlockControls();
};

function gatewayGetShifts(){
	var url = root +"/AjaxResponder?action=getShifts";
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystate = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				var shiftsHTML =gatewayParseShifts(xmlHttp.responseXML);
				setInnerHTML("upcomingShiftsList",shiftsHTML); // added semicolon
			}
			else {
				setInnerHTML("upcomingShiftsList", "Error Getting Users");
			}
		}
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function gatewayParseShifts(responseXML){
	var shifts = responseXML.getElementsByTagName("shifts")[0];
	var shiftsHTML = "You currently have no upcoming shifts";
	for (var i = 0; i < shifts.childNodes.length; i++) {
		var shift = shifts.childNodes[i];
		var shiftID = shift.childNodes[0].textContent;
		var department = shift.childNodes[1].textContent;
		var category = shift.childNodes[2].textContent;
		var location = shift.childNodes[3].textContent;
		var date = shift.childNodes[4].textContent;
		var startTime= shift.childNodes[5].textContent;
		var endTime	= shift.childNodes[6].textContent;
		var isForPermSale = shift.childNodes[7].textContent;
		var isForSale	= shift.childNodes[8].textContent;
		var permanentOwner	= shift.childNodes[9].textContent;
		var currentUser	= shift.childNodes[10].textContent;
			
		if (shiftsHTML == "You currently have no upcoming shifts"){
			shiftsHTML = "";
		}
		shiftsHTML += "<li>";
		shiftsHTML += "<table>";
		shiftsHTML += "<tr>";
		shiftsHTML += "<td>";
		shiftsHTML += "<span class='gCatName'>" + category + "</span> -";
		shiftsHTML += "<span class='gCatName'>" + location + "</span> -";
		shiftsHTML += "<span class='gDateInfo'>" + date + "</span>";
		shiftsHTML += "</br>";
		shiftsHTML += "<span class='gTimeInfo'>" + startTime + " to " + endTime + "</span>";
		shiftsHTML += "</td><td>";
		if(isForPermSale == "false" && permanentOwner == currentUser){
			shiftsHTML += "    <input type='button' class='smallMaroonButton' value='Permanently Sell This Shift' onclick='gatewayPermanentSellShift(\""+shiftID+"\", \""+date+"\", \""+category+"\", \""+department+"\")'"; 			
		}
		if(isForSale == "false"){
			shiftsHTML += "</br><input type='button' class='smallMaroonButton' value='Sell This Shift' onclick='gatewaySellShift(\""+shiftID+"\", \""+date+"\", \""+category+"\", \""+department+"\")'"; 
		}
		shiftsHTML += "</td></tr></table>";
		shiftsHTML += "</li>";
	}
	return shiftsHTML;
	
}

function getFiles() {
	var url = root +"/AjaxResponder?action=getFiles";
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				var response = xmlHttp.responseText;
				setInnerHTML("files", response);
			} else if(xmlHttp.status == 401) {
				 window.location = root +"/Login?action=goToLogin";
			} else {
				setInnerHTML("files", "No Files");
			}
		}
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function getCatNews() {
	var url = root +"/AjaxResponder?action=getCatNews";
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				var response = xmlHttp.responseText;
				setInnerHTML("catNewsList", response);
			}else if(xmlHttp.status == 401) {
				 window.location = root +"/Login?action=goToLogin";
			}
			else {
				setInnerHTML("catNewsList", "No News");
			}
		}
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function getDepNews() {
	var url =root + "/AjaxResponder?action=getDepNews";
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				var response = xmlHttp.responseText;
				setInnerHTML("depNewsList", response);
			}else if(xmlHttp.status == 401) {
				 window.location = root +"/Login?action=goToLogin";
			}
			else {
				setInnerHTML("depNewsList", "No News");
			}
			$("totalWrapper").style.display="inline";
		}
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

// get upcoming sales.
function getSales() {
	var url = root +"/AjaxResponder?action=getSales";
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				var response = xmlHttp.responseXML;
				// $("totalWrapper").style.display="none";
				var salesHTML = gatewayParseSales(response, false);
				setInnerHTML("shiftsForSaleList",salesHTML);
			}else if(xmlHttp.status == 401) {
				 window.location = root +"/Login?action=goToLogin";
			}
			else {
				setInnerHTML("shiftsForSaleList", "No Sales");
			}
			
		}
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

// get upcoming sales.
function getPermanentSales() {
	var url = root +"/AjaxResponder?action=getPermanentSales";
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				var response = xmlHttp.responseXML;
				// $("totalWrapper").style.display="none";
				var salesHTML = gatewayParseSales(response, true);
				setInnerHTML("shiftsForPermanentSaleList", salesHTML);
			}else if(xmlHttp.status == 401) {
				 window.location = root +"/Login?action=goToLogin";
			}
			else {
				setInnerHTML("shiftsForPermanentSaleList", "No Permanent Sales");
			}
		}
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function gatewayParseSales(responseXML, isPermanent){
	var sales = responseXML.getElementsByTagName("result")[0];
	var salesLength = sales.childNodes.length;
	var salesHTML = "There are currently no sales";
	for (var i = 0; i < salesLength; i++) {
		var sale = sales.childNodes[i];
		var shiftID = sale.childNodes[0].textContent;
		var category = sale.childNodes[1].textContent;
		var date = sale.childNodes[2].textContent;
		var startTime = sale.childNodes[3].textContent;
		var endTime = sale.childNodes[4].textContent;
		
		if (salesHTML == "There are currently no sales"){
			salesHTML = "";
		}
		salesHTML += "<li>";
		
		salesHTML += "<table>";
		salesHTML += "<tr>";
		salesHTML += "<td>";
		salesHTML += "<span class='gCatName'>" + category + "</span> -";
		salesHTML += "<span class='gDateInfo'>" + date + "</span>";
		salesHTML += "</br>";
		salesHTML += "<span class='gTimeInfo'>" + startTime + " to " + endTime + "</span>";
		salesHTML += "</td><td>";
		// the 1 in the buyShift function is there because that function
		// uses it to refresh part of the part the gateway page does not
		// and cant do that
		if(isPermanent){
			salesHTML += "<input type='button' class='smallMaroonButton' value='Permanently Buy This Shift' onclick='gatewayPermanentBuyShift("+shiftID+")'"; 
		} else {			
			salesHTML += "<input type='button' class='smallMaroonButton' value='Buy This Shift' onclick='gatewayBuyShift("+shiftID+")'"; 
		}
		salesHTML += "</td></tr></table>";
		salesHTML += "</li>";
	}
	return salesHTML;
}

// get list of users for shdraw
// -----------------------------is this still used
function getNames() {
	if(controlsLocked) {
		return;
	}
	lockControls();
	var url = root +  "/ShiftDraw?action=getNames";
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				var response = xmlHttp.responseText;
				setInnerHTML("namesList", response);
			}
			else {
				setInnerHTML("namesList", "Error: Server error or server not available");
			}
			unlockControls();
		}
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
	
	setTimeout('getNames()', 2000);
}

function changePasswordInit() {
	setInnerHTML("optionsTitle", "Change Password");
	var inner = "";
	inner += "<td class='optionsLabel' style='line-height: 2em;'>Old Password:<br>New Password:<br>Re-enter:<br></td>";
	inner += "<td class='optionsValue'><form name='pw'><input type='password' name='old'><br><input type='password' name='new1'><br><input type='password' name='new2'><br></form></input></td>";
	inner += "<td class='optionsAction'><span class='smallMaroonButton' onclick='changePassword();'>Change!</span></td>";
	setInnerHTML("optionsValues", inner);
	$("optionsDialog").style.display = "block";
}

function changePassword() {
	var url = root +  "/AjaxResponder";
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				alert("password successfully changed");
				$("optionsDialog").style.display = "none";
				setInnerHTML("optionsValues", "");
			}else if(xmlHttp.status == 401) {
				 window.location = root +"/Login?action=goToLogin";
			}
			else {
				alert("Incorrect Password");
			}
		}
	};
	var old = document.pw.old.value;
	var new1 = document.pw.new1.value;
	var new2 = document.pw.new2.value;
	if(new1 != new2) {
		alert("New Passwords must match!");
		return;
	}
	xmlHttp.open("POST", url, true);
	xmlHttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'); // RSL: Sets
		// the value of an HTTP request header. Must be called after open(), before send(). If called several
		// times with the same header, the values are merged into one single request header.
	xmlHttp.send("action=changePW&oldPW=" + old + "&newPW=" + new1);
}

function gatewayBuyShift(id) {
	if(controlsLocked)
		return;
	// first calc which row it'll be in.
	// okay, now send the request.
	lockControls();
	var url = root + "/ScheduleResponder?action=buy&id=" + id;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				gatewayGetShifts();
				getSales();	
			}
			else {
				setInnerHTML("shiftsForSaleList", "ERROR");
			}
		}
			
	};

	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
	unlockControls();
}


function gatewayPermanentBuyShift(id) {
	if(controlsLocked)
		return;
	// first calc which row it'll be in.
	// okay, now send the request.
	lockControls();
	var url = root +"/ScheduleResponder?action=pBuy&id=" + id;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				gatewayGetShifts();
				getPermanentSales();
			}
			else {
				setInnerHTML("forPermanentSale", "ERROR");
			}
		}
			
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
	unlockControls();
}

function gatewaySellShift(shiftID, date, category, department) {
	if(controlsLocked)
		return;
	lockControls();
	var url = root + "/AjaxResponder?action=sell&date=" + date + "&id=" + shiftID + "&department=" + department + "&category=" + category;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				alert("Shift was sold");
				gatewayGetShifts();
				gatewayGetSales();
			}
			else {
				setInnerHTML("shift" + id, "ERROR");
			}
		}
			
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
	unlockControls();
}


function gatewayPermanentSellShift(shiftID, day, date, category, department) {
	if(controlsLocked)
		return;
	
	// okay, now send the request.
	lockControls();
	var url = root +"/AjaxResponder?action=permanentlySell&date=" + date + "&id=" + shiftID + "&department=" + department + "&category=" + category;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				alert("Shift permanently was sold");
				gatewayGetShifts();
				getPermanentSales();
			}
			else {
				setInnerHTML("shift" + id, "ERROR");
			}
		}
			
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
	unlockControls();
}


// ************************************************************************************************************************************************
// ************************************************************************************************************************************************
// Start Of Gateway Administration Functions
// ************************************************************************************************************************************************
// ************************************************************************************************************************************************
function createUserInit() {
	setInnerHTML("optionsTitle", "Create User");
	var inner = "";
	inner += "<td class='optionsLabel' style='line-height: 2em;'>Username:<br>Password:<br>Re-enter:<br></td>";
	inner += "<td class='optionsValue'><form name='user1'><input type='text' name='username'><br><input type='password' name='new1'><br><input type='password' name='new2'><br></form></input></td>";
	inner += "<td class='optionsLabel' style='line-height: 2em;'>First Name:<br>Last Name:<br>Email:<br></td>";
	inner += "<td class='optionsValue'><form name='user2'><input type='text' name='fname'><br><input type='text' name='lname'><br><input type='text' name='email'><br></form></input></td>";
	inner += "<td class='optionsAction'><span class='smallMaroonButton' onclick='createUser();'>Create User</span></td>";
	setInnerHTML("optionsValues", inner);
	$("optionsDialog").style.display = "block";
}

function createUser() {
	var url = root + "/AjaxResponder";
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {

			if(xmlHttp.status == 200) {
				alert("user successfully created");
				$("optionsDialog").style.display = "none";
				setInnerHTML("optionsValues", "");
			}else if(xmlHttp.status == 401) {
				 window.location = root +"/Login?action=goToLogin";
			}
			else {
				alert("Error creating user");
			}
		}
	};
	var username = document.user1.username.value;
	var new1 = document.user1.new1.value;
	var new2 = document.user1.new2.value;
	if(new1 != new2) {
		alert("New Passwords must match!");
		return;
	}
	var fname = document.user2.fname.value;
	var lname = document.user2.lname.value;
	var email = document.user2.email.value;
	
	if(!alphanumeric(username)) {
		alert("Username must be alphanumeric");
		return;
	}
	
	xmlHttp.open("POST", url, true);
	xmlHttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'); 
	xmlHttp.send("action=createUser&username=" + username + "&pw=" + new1 + "&fname=" + fname + "&lname=" + lname + "&email=" + email);
}

function resetPWInit() {
	setInnerHTML("optionsTitle", "Reset Password");
	var inner = "";
	inner += "<td class='optionsLabel' style='line-height: 2em;'>Username:</td>";
	inner += "<td class='optionsValue'><form name='user1'><input type='text' name='username'><br></form></td>";
	inner += "<td class='optionsAction'><span class='smallMaroonButton' onclick='resetPW();'>Reset Password</span></td>";
	setInnerHTML("optionsValues", inner);
	$("optionsDialog").style.display = "block";
}

function resetPW() {
	var url = root +  "/AjaxResponder";
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				alert("password successfully reset");
				$("optionsDialog").style.display = "none";
				setInnerHTML("optionsValues", "");
			}else if(xmlHttp.status == 401) {
				 window.location = root +"/Login?action=goToLogin";
			}
			else {
				alert("Error Resetting Password");
			}
		}
	};
	var username = document.user1.username.value;
	
	xmlHttp.open("POST", url, true);
	xmlHttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'); 
	xmlHttp.send("action=resetPW&username=" + username);
}
// ------------------------------------------------------------------------------------------------------------------------------------------------
// End Of Gateway Administration Functions
// ------------------------------------------------------------------------------------------------------------------------------------------------

// ------------------------------------------------------------------------------------------------------------------------------------------------
// End Of Gateway Functions
// ------------------------------------------------------------------------------------------------------------------------------------------------





// ************************************************************************************************************************************************
// ************************************************************************************************************************************************
// Start Of General Ajax Support Functions
// ************************************************************************************************************************************************
// ************************************************************************************************************************************************

// Creates XMLHttpObject
function GetXmlHttpObject() { 
	if (navigator.userAgent.indexOf("MSIE")>=0) { 
		var strName="Msxml2.XMLHTTP";
		if (navigator.appVersion.indexOf("MSIE 5.5")>=0) {
			strName="Microsoft.XMLHTTP";
		} 
		try { 
			return new ActiveXObject(strName);
		} 	
		catch(e) { 
			alert("Error. Scripting for ActiveX might be disabled in your browser.") ;
			return;
		} 
	} 
	if (navigator.userAgent.indexOf("Mozilla")>=0) {
		return new XMLHttpRequest(); // RSL: constructor for initiating an XMLHttpRequest, must be called before any other method calls.
	}
}
// ------------------------------------------------------------------------------------------------------------------------------------------------
// End Of General Ajax Support Functions
// ------------------------------------------------------------------------------------------------------------------------------------------------






// ************************************************************************************************************************************************
// ************************************************************************************************************************************************
// Start Of Lab Availibity Functions
// ************************************************************************************************************************************************
// ************************************************************************************************************************************************
function updateAvailability() {
	var url = root+"/LabAvailability";
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == 4) {
			if (xmlHttp.status == 200) {
				parseAvailabilityResponse(xmlHttp.responseXML);
			}
			else if (xmlHttp.status == 204) {
				clearAvailability();
			}
		}
	};
	xmlHttp.open("GET",url,true);
	xmlHttp.send(null);
}

function parseAvailabilityResponse(responseXML) {
	var availability = responseXML.getElementsByTagName("availability")[0];
	for (var i = 0; i < availability.childNodes.length; i++) {
		var lab = availability.childNodes[i];
		var id = lab.getElementsByTagName("id")[0];
		var status = lab.getElementsByTagName("status")[0];
		setInnerHTML(id.childNodes[0].nodeValue,status.childNodes[0].nodeValue);		
	}
}

function clearAvailability() {
	setInnerHTML("poppaAvail","Unavailable");
	setInnerHTML("ktcAvail","Unavailable");
	setInnerHTML("southAvail","Unavailable");
}

function availabilityUpdateTimer() {
	updateAvailability();
	setTimeout("availabilityUpdateTimer()",60000);
}
// ------------------------------------------------------------------------------------------------------------------------------------------------
// End Of Lab Availibity Functions
// ------------------------------------------------------------------------------------------------------------------------------------------------






// ************************************************************************************************************************************************
// ************************************************************************************************************************************************
// Start Of Lab Map Functions
// ************************************************************************************************************************************************
// ************************************************************************************************************************************************
var aMapIsVisible = false;
var lta = false;

function setLtaMapView(l) {
	lta = l;
}

function showMap(lab) {
	showBlock('overlay');
	showBlock(lab + "Map");
	aMapIsVisible = true;
	mapUpdateTimer();
}

function hideMap(id) {
	aMapIsVisible = false;
	hide(id);
	hide('overlay');
}

function hideOverlay() {
	hide('overlay');
}

function updateMaps(lta) {
	var url = root+"/LabMap";
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == 4) {
			if (xmlHttp.status == 200) {
				parseMapResponse(xmlHttp.responseXML,lta);
			}
			else if (xmlHttp.status == 204) {
				clearMaps();
			}
		}
	};
	xmlHttp.open("GET",url,true);
	xmlHttp.send(null);
}

function parseMapResponse(responseXML,lta) {
	var stations = responseXML.getElementsByTagName("stations")[0];
	for (var i = 0; i < stations.childNodes.length; i++) {
// alert("Current ID " + id.childNodes[0].nodeValue);
		var station = stations.childNodes[i];
		var id = station.getElementsByTagName("id")[0];
		var label = station.getElementsByTagName("label")[0];
		var status = station.getElementsByTagName("status")[0];
		updateStation(label.childNodes[0].nodeValue, id.childNodes[0].nodeValue,status.childNodes[0].nodeValue);
// alert(id.childNodes[0].nodeValue+ " is done");
	}
}

// Possible map inside texts
var available = "Available";
var inUse = "In Use";
var locked = "Locked";
var shutdown = "Shutdown";
var closedForMaintenance = "Closed For Maintenance";
// var ltaStation = "LTA Station";

// Possible map background colors
var availableBG = "#E5E5E5";
var inuseBG = "#74BBFB";
var lockedBG = "#DA4747";
var shutdownBG = "#8B8B7A";
var maintenanceBG = "#FF6600";

function updateStation(label, id, status) {
	var color;
	
	if (status == available) {
		color = availableBG;
	}else if (status.indexOf(locked) != -1){
		color = lockedBG;
	} else if (status == shutdown){
		color = shutdownBG;
	} else if (status == closedForMaintenance){
		color = maintenanceBG;
	} else {
		color = inuseBG;
	}

	// This should be done on the server side
	// if ((id == "poppa16" || id == "ktc0") && !lta) {
	// status = ltaStation;
	// }
	setInnerHTML(id,label + "<br/>"+ status);

	$(id).style.backgroundColor = color;
}

function clearMaps() {
	for (var i = 1; i < 36; i++) {
		setInnerHTML("poppa" + i,"Unavailable");
	}
	for (var i = 0; i < 17; i++) {
		setInnerHTML("ktc" + i,"Unavailable");
	}
	for (var i = 1; i < 15; i++) {
		setInnerHTML("south" + i,"Unavailable");
	}	
}

function setLastUpdated() {
	var now;
	var currentTime = new Date();
	var month = currentTime.getMonth() + 1;
	var day = currentTime.getDate();
	var year = currentTime.getFullYear();
	
	var hours = currentTime.getHours();
	var minutes = currentTime.getMinutes();
	var seconds = currentTime.getSeconds();
	
	if (seconds < 10) 
		seconds = "0" + seconds;
	
	if (minutes < 10) 
		minutes = "0" + minutes;
	
	var ampm; 
	if (hours > 11)
		ampm = "PM";
	else
		ampm = "AM";
		
	if (hours == 0)
		hours = "12";
	else if (hours > 12) 
		hours = hours - 12;
	else 
		hours = "0" + hours;
	
	now = month + "/" + day + "/" + year + " " + hours + ":" + minutes + " " + ampm;
	
	setInnerHTML('poppaLastUpdated',"Updated: " + now);
	setInnerHTML('ktcLastUpdated',"Updated: " + now);
	setInnerHTML('southLastUpdated',"Updated: " + now);
}

function mapUpdateTimer() {
	updateMaps(lta);
	setLastUpdated();
	if (aMapIsVisible) {
		setTimeout("mapUpdateTimer(" + lta + ")",60000);
	}
}

function loadLabStatus() {
	var labs = new Array('poppaStatus','ktcStatus','southStatus', 'rrlStatus');
	var url = root+ "/LabStatus?action=getAllLabStatus";
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == 4) {
			if (xmlHttp.status == 200) {
				var ls = xmlHttp.responseXML.getElementsByTagName("labs")[0];
				for (var i = 0; i < ls.childNodes.length; i++) {
					var lab = ls.childNodes[i];
					var status = lab.getElementsByTagName("status")[0];
					setInnerHTML(labs[i],status.childNodes[0].nodeValue);
				}
			}
		}
	};
	xmlHttp.open("GET",url,true);
	xmlHttp.send(null);
	setTimeout('loadLabStatus()',180000);
}
// ------------------------------------------------------------------------------------------------------------------------------------------------
// End Of Lab Availibity Functions
// ------------------------------------------------------------------------------------------------------------------------------------------------








// ************************************************************************************************************************************************
// ************************************************************************************************************************************************
// Start Of Schedule Functions
// ************************************************************************************************************************************************
// ************************************************************************************************************************************************
var isSchedule = false;
var isGate = false;
var isMapRotator = false;
var activeDepartment = "";
var activeCategory = "";
var dayIndex = -1;
var currDep;
var currCat;
var controlsLocked = false;
var rowsCount = 0;

function lockControls() {
	controlsLocked = true;
}
function unlockControls() {
	controlsLocked = false;
}

function changeDepartmentCategory(dropdown){
	if(controlsLocked) {
		return;
	}
	lockControls();
	var myindex  = dropdown.selectedIndex;
    var dropdownValue = dropdown.options[myindex].value;
    var invalidSelection = dropdownValue.indexOf("NOCHANGE") != -1;
    if(invalidSelection){
    	return;
    }
    var department = dropdownValue.split(":")[0];
    var category = dropdownValue.split(":")[1];
    unlockControls();
    changeCategory(department, category);
}

function changeCategory(department, category) {
	if(controlsLocked) {
		return;
	}
	lockControls();
	currDep = department;
	currCat = category;
	var url;
	if(isSchedule) {
		url = root + "/ScheduleResponder?action=changeCat&dep=" + department + "&cat=" + category;
	}
	else {
		url = root + "/AjaxResponder?action=changeCat&dep=" + department + "&cat=" + category;
		if(currDep=="Mail Room"){
			$(MailRoomAdminBox).style.visibility='visible';
		}
	}
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				var response = xmlHttp.responseXML;
				displayTabsBar(response);
				if(isSchedule) {
					dayIndex = -1;
					// display 7 days of shifts.
					getAllRows(-1);
				}
				
			}else if(xmlHttp.status == 401) {
				 window.location = root +"/Login?action=goToLogin";
			}
			else {
				setInnerHTML("tabs", "Error: Server error or server not available");
			}
			unlockControls();
			gatewayGetAllInformation(); //added semicolon
		}
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function displayRow(row, xmlResp) {
	closeShiftOptions();
	var day = xmlResp.getElementsByTagName("day")[0].firstChild.nodeValue;

	var date = xmlResp.getElementsByTagName("date")[0].firstChild.nodeValue;
	var rightInner = "<div class='rowDate'>" + date + "</div>";
	setInnerHTML("r" + row, rightInner);
	setInnerHTML("day" + row, day);
	var locsInner = "";
	var shiftsInner = "";
	for(var i = 0; i < xmlResp.getElementsByTagName("loc").length; i++) {
		// display locations. xmlResp.childNodes[i] should be a
		// <location>...</location> element
		// first get location name.
		var loc = xmlResp.getElementsByTagName("loc")[i].getElementsByTagName("name")[0].firstChild.nodeValue;
		locsInner += "<tr><td class='locName'>" + loc + "</td></tr>";
		shiftsInner += "<table id=\"sh" + row + "" + i + "\"class=\"locArea\"><tr>"; 
		
		var sh = [];
		// this will hold subarrays
		// in the form id, startTime, endtime, startdate, enddate, owner, buyer,
		// sold, beginmins, durmins, state, buy, sell, pbuy, psell
		// to put it into a more readable form.
		for(var j = 0; j < xmlResp.getElementsByTagName("loc")[i].getElementsByTagName("shift").length; j++) {
			var shifts = xmlResp.getElementsByTagName("loc")[i].getElementsByTagName("shift")[j];
			var inf = [];
			inf[0] = shifts.getElementsByTagName("shiftID")[0].firstChild.nodeValue;
			inf[1] = shifts.getElementsByTagName("startTime")[0].firstChild.nodeValue;
			inf[2] = shifts.getElementsByTagName("endTime")[0].firstChild.nodeValue;
			inf[3] = shifts.getElementsByTagName("startDate")[0].firstChild.nodeValue;
			inf[4] = shifts.getElementsByTagName("endDate")[0].firstChild.nodeValue;
			if(shifts.getElementsByTagName("owner")[0].firstChild != null) {
				inf[5] = shifts.getElementsByTagName("owner")[0].firstChild.nodeValue;
			}
			else {
				inf[5] = "??";
			}
			if(shifts.getElementsByTagName("buyer")[0].firstChild != null) {
				inf[6] = shifts.getElementsByTagName("buyer")[0].firstChild.nodeValue;
			}
			else {
				inf[6] = "??";
			}
			if(shifts.getElementsByTagName("sold")[0].firstChild != null) {
				inf[7] = shifts.getElementsByTagName("sold")[0].firstChild.nodeValue;
			}
			else {
				inf[7] = "??";
			}
			inf[8] = shifts.getElementsByTagName("beginMins")[0].firstChild.nodeValue;
			inf[9] = shifts.getElementsByTagName("durMins")[0].firstChild.nodeValue;
			inf[10] = shifts.getElementsByTagName("state")[0].firstChild.nodeValue;
			inf[11] = shifts.getElementsByTagName("buy")[0].firstChild.nodeValue;
			inf[12] = shifts.getElementsByTagName("sell")[0].firstChild.nodeValue;
			inf[13] = shifts.getElementsByTagName("pBuy")[0].firstChild.nodeValue;
			inf[14] = shifts.getElementsByTagName("pSell")[0].firstChild.nodeValue;
			inf[15] = shifts.getElementsByTagName("activate")[0].firstChild.nodeValue;
			inf[16] = shifts.getElementsByTagName("assign")[0].firstChild.nodeValue;
			inf[17] = shifts.getElementsByTagName("pAssign")[0].firstChild.nodeValue;
			inf[18] = shifts.getElementsByTagName("shiftDraw")[0].firstChild.nodeValue;
			inf[19] = shifts.getElementsByTagName("deactivate")[0].firstChild.nodeValue;
			// inf[20] =
			// shifts.getElementsByTagName("modify")[0].firstChild.nodeValue;
			sh[j] = inf;
		}
		// now write the shift info.
		// shifts sorted by time, thankfully.
		
		var currPercent = 0;
		for(j = 0; j < sh.length; j++) {
			var toBeg = sh[j][8]/60;
			toBeg += 2;
			var dur = sh[j][9]/60;
			var perToBeg = Math.floor(  (toBeg-startDisp)/(endDisp-startDisp)*100  );
			if(((toBeg-startDisp)/(endDisp-startDisp)*100) - perToBeg >= .5) {
				perToBeg++;
			}
			if(perToBeg != currPercent) {
				spacerPer = perToBeg - currPercent;
				shiftsInner += "<td width='" + spacerPer + "%' class='spacer'></td>";
				currPercent = perToBeg;
			}
			
			var perToEnd = Math.floor(  (toBeg + dur - startDisp)/(endDisp-startDisp)*100  );
			if((toBeg + dur - startDisp)/(endDisp-startDisp)*100 - perToEnd >= .5) {
				perToEnd++;
			}
			var shPer = perToEnd - currPercent;
			shiftsInner += "<td width='" + shPer + "%'><div onclick=\"showShiftOptions(" + sh[j][0] + ");\" id=\"shift" + sh[j][0] + "\" class=\"";
			currPercent = perToEnd;
			
			switch(sh[j][10]) {
				case "0":
					shiftsInner += "shiftInactive";
					break;
				case "1":
					shiftsInner += "shiftNormal";
					break;
				case "2":
					shiftsInner += "shiftSale";
					break;
				case "3":
					shiftsInner += "shiftPSale";
					break;
				case "4":
					shiftsInner += "shiftSPSale";
					break;
				default:
					shiftsInner += "shiftInactive";
					break;
			}
			shiftsInner += "\">";
			
			if(sh[j][6] != null && sh[j][6] != "??") {
				shiftsInner += sh[j][6].substring(0,2).toUpperCase() + "(" + sh[j][5].substring(0,2).toUpperCase() + ")";
			}
			else if(sh[j][7] != null && sh[j][7] != "??") {
				shiftsInner += sh[j][5].substring(0,2).toUpperCase();
			}
			else if(sh[j][5] != null && sh[j][5] != "??") {// this is
															// proprietary
				if(sh[j][5] == "LTA") {
					shiftsInner += "*ALL*";
				}
				else {
					shiftsInner += sh[j][5].substring(0,2).toUpperCase();
				}
			}
			else {
				shiftsInner += "??";
			}
			shiftsInner += "</div></td>";
			
// shiftsInner += "<form name=\"shift" + sh[j][0] + "info\">";
			shiftsInner += "<input type=\"hidden\" name=\"startTime\" id=\"startTimeInfoOnShift"+ sh[j][0] +"\" value=\"" + sh[j][1] + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"endTime\" id=\"endTimeInfoOnShift"+ sh[j][0] +"\" value=\"" + sh[j][2] + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"startDate\"  id=\"startDateInfoOnShift"+ sh[j][0] +"\" value=\"" + sh[j][3] + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"endDate\"  id=\"endDateInfoOnShift"+ sh[j][0] +"\" value=\"" + sh[j][4] + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"owner\"  id=\"ownerInfoOnShift"+ sh[j][0] +"\" value=\"" + sh[j][5] + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"buyer\"  id=\"buyerInfoOnShift"+ sh[j][0] +"\" value=\"" + sh[j][6] + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"sold\"  id=\"soldInfoOnShift"+ sh[j][0] +"\" value=\"" + sh[j][7] + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"buy\"  id=\"buyInfoOnShift"+ sh[j][0] +"\" value=\"" + sh[j][11] + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"sell\"  id=\"sellInfoOnShift"+ sh[j][0] +"\" value=\"" + sh[j][12] + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"pBuy\"  id=\"pBuyInfoOnShift"+ sh[j][0] +"\" value=\"" + sh[j][13] + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"pSell\"  id=\"pSellInfoOnShift"+ sh[j][0] +"\" value=\"" + sh[j][14] + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"day\"  id=\"dayInfoOnShift"+ sh[j][0] +"\" value=\"" + day + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"loc\"  id=\"locInfoOnShift"+ sh[j][0] +"\" value=\"" + loc + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"date\"  id=\"dateInfoOnShift"+ sh[j][0] +"\" value=\"" + date + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"dayInd\"  id=\"dayIndInfoOnShift"+ sh[j][0] +"\" value=\"" + (row+dayIndex) + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"activate\"  id=\"activateInfoOnShift"+ sh[j][0] +"\" value=\"" + sh[j][15] + "\">";
			
			shiftsInner += "<input type=\"hidden\" name=\"deactivate\"  id=\"deactivateInfoOnShift"+ sh[j][0] +"\" value=\"" + sh[j][19] + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"assign\"  id=\"assignInfoOnShift"+ sh[j][0] +"\" value=\"" + sh[j][16] + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"pAssign\"  id=\"pAssignInfoOnShift"+ sh[j][0] +"\" value=\"" + sh[j][17] + "\">";
			shiftsInner += "<input type=\"hidden\" name=\"shiftDraw\" id=\"shiftDrawInfoOnShift"+ sh[j][0] +"\"  value=\"" + sh[j][18] + "\">";
			
			// shiftsInner += "<input type=\"hidden\" name=\"shiftDraw\"
			// value=\"" + sh[j][20] + "\">";
// shiftsInner += "</form>";
		}
		shiftsInner += "<td width=\"" + (100-currPercent) + "%\" class=\"spacer\"></td>";
		shiftsInner += "</tr></table>";
	}
	setInnerHTML("locs" + row, locsInner);
	setInnerHTML("m" + row, shiftsInner);
}

function getShiftRow(day, row) {
	lockControls();
	var url = root + "/ScheduleResponder?action=getRow&day=" + day;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				var response = xmlHttp.responseXML;
				displayRow(row, response);
			}
			else {
				setInnerHTML("m" + row, "Error: Server error or server not available");
			}
			unlockControls();
		}
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function getAllRows(day) {
	getRows(day, 7, 0);
}

function getAll() {
	getRows(dayIndex, 7, 0);
}

function getRows(day, num, ind) {
	// no lock, always called secondarily.
	var url = root + "/ScheduleResponder?action=getRows&day=" + day + "&num=" + num;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				var response = xmlHttp.responseXML;
				var rows = response.getElementsByTagName("row");
				for(var a = 0; a < rows.length; a++) {
					displayRow(a + ind, rows[a]);
				}
			}
			else {
				alert("Error: Internal server error or server not available");
			}
			// make sure to lock controls again if more commands needed!
			unlockControls();
		}
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function nav(numOfDays) {
	lockControls();
	closeShiftOptions();
	// if(numOfDays == 1) {
		// better to swap
	// }
	// else if(numOfDays == -1) {
		// also better to swap
	// }
	// else {
		dayIndex += numOfDays;
		getRows(dayIndex, 7, 0);
	// }
	// controls will be unlocked by getRows
}

function showScheduleRows(numOfRows) {
	var inner = "";
	for(var i = 0; i < numOfRows; i++) {
		inner += "<tr><table id=\"row" + i + "\" class=\"totalRow\"><td id=\"l" + i + "\" class=\"leftCol\"><table class=\"leftTable\"><tr><td class=\"rowDay\" id=\"day" + i + "\" width=40%></td><td class=\"locNameWrap\"width=60%><table id=\"locs" + i + "\"></table></td></tr></table></td><td id=\"m" + i + "\" class=\"mainCol\">Loading...</td><td id=\"r" + i + "\" class=\"rightCol\"></td></table></tr>";
	}
	rowsCount = numOfRows;
	setInnerHTML("scheduleRowHolder", inner);
}

var currentShiftOpen = -1;

function showShiftOptions(shiftNum) {
	$("shift"+shiftNum).style.border="3px #990000 solid";
	$("shift"+shiftNum).style.padding="1px";
	if(currentShiftOpen != -1) {
		$("shift"+currentShiftOpen).style.border = null;
		$("shift"+currentShiftOpen).style.padding = null;
	}
	if(currentShiftOpen == shiftNum) {
		// CLOSE THE SHIFT OPTIONS THING
		closeShiftOptions();
		return;
	}
	if(currentShiftOpen == -1) {
	}
	currentShiftOpen = shiftNum;
	// now display the stuff
	setInnerHTML("optionsTitle", "Shift Details");
	var headings = 	"<td colspan=2>Ownership</td><td colspan=2>Time</td><td colspan=2>Date</td><td colspan=2>Location</td>";
	var num = 0;
	
	var opts = false;
	var aOpts = false;
	
	if(document.getElementById('buyInfoOnShift'+shiftNum).value == "true")
		num++;
	if(document.getElementById('sellInfoOnShift'+shiftNum).value == "true")
		num++;
	if(document.getElementById('pBuyInfoOnShift'+shiftNum).value == "true")
		num++;
	if(document.getElementById('pSellInfoOnShift'+shiftNum).value == "true")
		num++;
	if(document.getElementById('shiftDrawInfoOnShift'+shiftNum).value == "true")
		num++;
	if(num != 0) {
		// now we have the number of commands available.
		var rem = num%3;
		var toAdd = (3-rem)%3;
		num += toAdd;
		numCols = num/3;
		headings += "<td colspan=" + numCols + ">Options</td>";
		opts = true;
	}
	
	num = 0;
	if(document.getElementById('activateInfoOnShift'+shiftNum).value == "true")
		num++;
	if(document.getElementById('deactivateInfoOnShift'+shiftNum).value == "true")
		num++;
	if(document.getElementById('assignInfoOnShift'+shiftNum).value == "true")
		num++;
	if(num != 0) {
		// now we have the number of commands available.
		var rem = num%3;
		var toAdd = (3-rem)%3;
		num += toAdd;
		numCols = num/3;
		headings += "<td colspan=" + numCols + ">Admin Options</td>";
		aOpts = true;
	}
	
	setInnerHTML("optionsHeadings", headings);
	
	// now for actual info.
	
	var infVals = "";
	infVals += "<td class='optionsLabel'>Owner:<br>This Shift:<br>Sale Posted:<br>";
	infVals += "<td class='optionsValue'>";
	infVals += document.getElementById('ownerInfoOnShift'+shiftNum).value + "<br>";
	infVals += document.getElementById('buyerInfoOnShift'+shiftNum).value + "<br>";
	infVals += document.getElementById('soldInfoOnShift'+shiftNum).value + "<br>";
	infVals += "</td>";
	
	infVals += "<td class='optionsLabel'>Day:<br>Start Time:<br>End Time:<br>";
	infVals += "<td class='optionsValue'>";
	infVals += document.getElementById('dayInfoOnShift'+shiftNum).value + "<br>";
	infVals += document.getElementById('startTimeInfoOnShift'+shiftNum).value + "<br>";
	infVals += document.getElementById('endTimeInfoOnShift'+shiftNum).value + "<br>";
	infVals += "</td>";
	
	infVals += "<td class='optionsLabel'>Date:<br>Starts:<br>Ends:<br>";
	infVals += "<td class='optionsValue'>";
	infVals += document.getElementById('dateInfoOnShift'+shiftNum).value + "<br>";
	infVals += document.getElementById('startDateInfoOnShift'+shiftNum).value + "<br>";
	infVals += document.getElementById('endDateInfoOnShift'+shiftNum).value + "<br>";
	infVals += "</td>";
	
	infVals += "<td class='optionsLabel'>Department:<br>Category:<br>Location:<br>";
	infVals += "<td class='optionsValue'>";
	infVals += activeDepartment + "<br>";
	infVals += activeCategory + "<br>";
	infVals += document.getElementById('locInfoOnShift'+shiftNum).value + "<br>";
	infVals += "</td>";
	
	// and now for options.
	var numInCol = 0;
	
	if(opts) {
		infVals += "<td class='optionsAction'>";
		
		//added date
		if(document.getElementById('buyInfoOnShift'+shiftNum).value == "true") {
			infVals += "<span class='schOption' onclick='buyShift(" + document.getElementById('dayIndInfoOnShift'+shiftNum).value + ", " + shiftNum + "," + document.getElementById('dateInfoOnShift'+shiftNum).value + ");'>Buy Shift</span><br>";
			
			numInCol++;
		}
		
		//added date
		if(document.getElementById('sellInfoOnShift'+shiftNum).value == "true") {
			infVals += "<span class='schOption' onclick='sellShift(" + document.getElementById('dayIndInfoOnShift'+shiftNum).value + ", " + shiftNum + ","+ document.getElementById('dateInfoOnShift'+shiftNum).value + ");'>Sell Shift</span><br>";
			numInCol++;
		}
		if(document.getElementById('pBuyInfoOnShift'+shiftNum).value == "true") {
			infVals += "<span class='schOption' onclick='pBuyShift(" + document.getElementById('dayIndInfoOnShift'+shiftNum).value + ", " + shiftNum + ");'>Perm Buy</span><br>";
			
			numInCol++;
		}
		if(document.getElementById('pSellInfoOnShift'+shiftNum).value == "true") {
			if(numInCol == 3) {	
				numInCol = 0;	
				infVals += "</td><td class='optionsAction'>";
			}
			infVals += "<span class='schOption' onclick='pSellShift(" +document.getElementById('dayIndInfoOnShift'+shiftNum).value+ ", " + shiftNum + ");'>Perm Sell</span><br>";
			numInCol++;
		}
		if(document.getElementById('shiftDrawInfoOnShift'+shiftNum).value == "true") {
			if(numInCol == 3) {
				numInCol = 0;
				infVals += "</td><td class='optionsAction'>";
			}
			infVals += "<span class='schOption' onclick='drawShift(" +document.getElementById('dayIndInfoOnShift'+shiftNum).value + ", " + shiftNum + ");'>Shift Draw</span><br>";
			numInCol++;
		}
	
		
		infVals += "</td>";
	}
	
	// NOW FOR ADMIN OPTIONS
	numInCol = 0;
	
	if(aOpts) {
		infVals += "<td class='optionsAction'>";
		
		if(document.getElementById('activateInfoOnShift'+shiftNum).value == "true") {
			infVals += "<span class='schOption' onclick='activateShift(" + document.getElementById('dayIndInfoOnShift'+shiftNum).value + ", " + shiftNum + ");'>Activate</span><br>";
			numInCol++;
		}
		if(document.getElementById('deactivateInfoOnShift'+shiftNum).value == "true") {
			infVals += "<span class='schOption' onclick='deactivateShift(" +document.getElementById('dayIndInfoOnShift'+shiftNum).value+ ", " + shiftNum + ");'>Deactivate</span><br>";
			numInCol++;
		}
		if(document.getElementById('assignInfoOnShift'+shiftNum).value == "true") {
			infVals += "<span class='schOption' onclick='assignShiftInit(" +document.getElementById('dayIndInfoOnShift'+shiftNum).value + ", " + shiftNum + ");'>Assign Shift</span><br>";
			numInCol++;
		}
		if(document.getElementById('pAssignInfoOnShift'+shiftNum).value == "true") {
			infVals += "<span class='schOption' onclick='pAssignShiftInit(" + document.getElementById('dayIndInfoOnShift'+shiftNum).value + ", " + shiftNum + ");'>Perm Assign</span><br>";
		}
	
	}	
	
	setInnerHTML("optionsValues", infVals);
	
	$("optionsDialog").style.display = "block";
	
	setInnerHTML("optionsX", "<div class='x' onclick='showShiftOptions(" + shiftNum + ");'>X</div>");
}


function closeShiftOptions() {
	currentShiftOpen = -1;
	$("optionsDialog").style.display = "none";
}

function showTabs() {
lockControls();
	var url;
	if(isSchedule) {
		url = root + "/ScheduleResponder?action=getCats";
	}
	else {
		url = root + "/AjaxResponder?action=getCategories";
	}
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				var response = xmlHttp.responseXML;
				displayTabsBar(response);
			}else if(xmlHttp.status == 401) {
				 window.location = root +"/Login?action=goToLogin";
			}
			else {
				setInnerHTML("tabs", "Error: Server error or server not available!");
			}
			unlockControls();
		}	
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function displayTabsBar(xmlResp) {
	var deps = xmlResp.getElementsByTagName("department");
	var inner = "";
	inner += "<div id='depSelector'>";
	inner += "<form name='dept'>";
	inner += "<select name='department' onchange=changeDepartmentCategory(this.form.department)>";
	inner += "<option value='NOCHANGE'>Select a Category</option>";
	inner += "<option value='NOCHANGE'>----------------</option>";
	var innerTabs = "";
	for(var i = 0; i < deps.length; i++) {
		if(deps[i].getElementsByTagName("active")[0].firstChild != null 
				&& deps[i].getElementsByTagName("active")[0].firstChild.nodeValue == "true") {
			// show tabs too, set selected
			var depName = deps[i].getElementsByTagName("name")[0].firstChild.nodeValue;
			inner += "<option value='" + depName + "' selected>&nbsp;[" + depName + "]</option>";
			activeDepartment = depName;
			if(isGate)
				setInnerHTML("depName", depName);
			var cats = deps[i].getElementsByTagName("category");
			for(var j = 0; j < cats.length; j++) {
				var catName = cats[j].getElementsByTagName("name")[0].firstChild.nodeValue;
				if(cats[j].getElementsByTagName("active")[0].firstChild != null && cats[j].getElementsByTagName("active")[0].firstChild.nodeValue == "true") {
					// active cat
					innerTabs += "<div class='catTabActive'>" + catName + "</div>";
					inner += "<option value='" + depName + ":" + catName + "'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + catName + "</option>";
					activeCategory = catName;
					if(isGate)
						setInnerHTML("catName", catName);
					
				}
				else {
					innerTabs += "<div class='catTab' " + (isSchedule ? "" : "style='width: 5em;'") + "onclick='changeCategory(\"" + depName + "\", \"" + catName + "\");'>" + catName + "</div>";
					inner += "<option value='" + depName + ":" + catName + "' >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + catName + "</option>";
				}
			}
				
		}
		else {
			// just add to the dropdown
			var depName = deps[i].getElementsByTagName("name")[0].firstChild.nodeValue;
			inner += "<option value='" + depName + "'>&nbsp;[" + depName + "]</option>";
			
			var cats = deps[i].getElementsByTagName("category");
			for(var j = 0; j < cats.length; j++) {
				var catName = cats[j].getElementsByTagName("name")[0].firstChild.nodeValue;
				inner += "<option value='"+ depName + ":" + catName + "' >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + catName + "</option>";
			}
		}
	}
	inner += "</select></form>";
	inner += "</div>";
	inner += innerTabs;
	setInnerHTML("tabs", inner);
	
	if(isGate) {
	
	
		var adminOpts = false;
		var runShiftDraw = false;
		var createUser = false;
		var createShift = false;
		var resetPW = false;
	
		if(xmlResp.getElementsByTagName("runShiftDraw")[0].firstChild.nodeValue == "true") {
			adminOpts = true;
			runShiftDraw = false;//Note that this is set to false to make the runshift draw now appear
		}
		if(xmlResp.getElementsByTagName("createUser")[0].firstChild.nodeValue == "true") {
			adminOpts = true;
			createUser = true;
		}
		if(xmlResp.getElementsByTagName("createShift")[0].firstChild.nodeValue == "true") {
			adminOpts = true;
			createShift = true;
		}
		if(xmlResp.getElementsByTagName("resetPW")[0].firstChild.nodeValue == "true") {
			adminOpts = true;
			resetPW = true;
		}
		
		
		
		var optsInner = "";
		optsInner += "<li><a onclick='changePasswordInit()'>Change Password</a></li>";
		setInnerHTML("depUserOpts", optsInner);
		
		if(adminOpts) {	
			var admInner = "<span class=\"listByTitle\">Admin Options</span><ul>";
			if(runShiftDraw) {
				admInner += "<li><a href='/ShiftDraw' target='_blank'>Run Shift Draw</a></li>";
			}
			if(createUser) {
				admInner += "<li><a href='http://stat/Login?action=goToRegistration'>Create User</a></li>";
			}
			if(createShift) {
				admInner += "<li><a onclick='uploadShiftCSVInit();'>Upload Shifts (.csv)</li>";
			}
			if(resetPW) {
				admInner += "<li><a onclick='resetPWInit();'>Reset Password</li>";
			}
			setInnerHTML("adminOpts", admInner+"</ul>");
		}
	}
}
function showTimeMarks() {
	var currTime = startDisp;
	var inner = "";
	var currPercent = 0;
	while(currTime < endDisp) {
		inner += "<td class='timeStamp' width='";
		var totalPercent = Math.floor((currTime+1-startDisp)/(endDisp-startDisp)*100);
		if(((currTime+1-startDisp)/(endDisp-startDisp)*100) - totalPercent >= .5) {
			totalPercent++;
		}
		inner += (totalPercent-currPercent) + "%'>|" + (currTime%12 == 0 ? 12 : currTime%12);
		inner += "</td>";
		currTime++;
		currPercent = totalPercent;
		
	}
	setInnerHTML("timeMarksTR", inner);
}

/** BUY/SELL ETC* */
function buyShift(day, id, date) {
	if(controlsLocked)
		return;
	// first calc which row it'll be in.
	var row = day - dayIndex;
	// okay, now send the request.
	//lockControls();
	//added date
	var url = root + "/ScheduleResponder?action=buy&id=" + id+"&date="+day;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				// var response = xmlHttp.responseXML;
				getShiftRow(day, row);
			}
			else {
				setInnerHTML("shift" + id, "ERROR");
			}
		}
			
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function sellShift(day, id, date) {

	
	if(controlsLocked)
		return;
	// first calc which row it'll be in.
	var row = day - dayIndex;
	// okay, now send the request.
	lockControls();
	var url = root + "/ScheduleResponder?action=sell&date=" + day + "&id=" + id;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				// var response = xmlHttp.responseXML;
				getShiftRow(day, row);
			}
			else {
				setInnerHTML("shift" + id, "ERROR");
			}
		}
			
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function pBuyShift(day, id) {
	if(controlsLocked)
		return;
	// first calc which row it'll be in.
	var row = day - dayIndex;
	// okay, now send the request.
	lockControls();
	var url = root +"/ScheduleResponder?action=pBuy&id=" + id;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				// var response = xmlHttp.responseXML;
				getShiftRow(day, row);
			}
			else {
				setInnerHTML("shift" + id, "ERROR");
			}
		}
			
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function pSellShift(day, id) {
	if(controlsLocked)
		return;
	// first calc which row it'll be in.
	var row = day - dayIndex;
	// okay, now send the request.
	lockControls();
	var url = root +"/ScheduleResponder?action=pSell&day=" + day + "&id=" + id;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				// var response = xmlHttp.responseXML;
				getShiftRow(day, row);
			}
			else {
				setInnerHTML("shift" + id, "ERROR");
			}
		}
			
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function activateShift(day, id) {
	if(controlsLocked)
		return;
	// first calc which row it'll be in.
	var row = day - dayIndex;
	// okay, now send the request.
	lockControls();
	var url = root +"/ScheduleResponder?action=activate&day=" + day + "&id=" + id;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				// var response = xmlHttp.responseXML;
				getShiftRow(day, row);
			}
			else {
				setInnerHTML("shift" + id, "ERROR");
			}
		}
			
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function deactivateShift(day, id) {
	if(controlsLocked)
		return;
	// first calc which row it'll be in.
	var row = day - dayIndex;
	// okay, now send the request.
	lockControls();
	var url = root +"/ScheduleResponder?action=deactivate&day=" + day + "&id=" + id;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				// var response = xmlHttp.responseXML;
				getShiftRow(day, row);
			}
			else {
				setInnerHTML("shift" + id, "ERROR");
			}
		}
			
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function parseUsers(responseXML){
	var response = responseXML.getElementsByTagName("result")[0];
	var users = new Array();
	for (var i = 0; i < response.childNodes.length; i++) {
		var userFirstLastNames = response.childNodes[i].textContent;
		users[i] = userFirstLastNames;		
	}
	return users;
}

function assignShiftInit(day, id){
	var url = root +"/ScheduleResponder?action=getUsers&date="+day;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				var users = parseUsers(xmlHttp.responseXML);
				
				setInnerHTML("optionsHeadings", "<td colspan=0>Users</td>");
				var inner = "<td class='optionsAction'>";
				for(var i = 0; i < users.length; i++) {
					if(i%5 == 0 && i != 0) {
						inner += "</td><td class='optionsAction'>";
					}
					inner += "<span class='schOption' onclick='assignShift(" + day + ", " + id + ", \"" + users[i].split(":")[0] + "\");'>" + users[i].split(":")[1] + "</span><br>";
				}
				// add the update button
				
				inner += "</td>";
				setInnerHTML("optionsValues", inner);
			}
			else {
				setInnerHTML("shift" + id, "Error Getting Users");
			}
		}
			
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function assignShift(day, id, user) {
	if(controlsLocked)
		return;
	// first calc which row it'll be in.
	var row = day - dayIndex;
	
	// okay, now send the request.
	lockControls();
	var url = root +"/ScheduleResponder?action=assign&day=" + day + "&id=" + id + "&new=" + user;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				// var response = xmlHttp.responseXML;
				getShiftRow(day, row);
			}
			else {
				setInnerHTML("shift" + id, "ERROR");
			}
		}
			
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function pAssignShiftInit(day, id) {
	var url = root +"/ScheduleResponder?action=getUsers";
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				var users = parseUsers(xmlHttp.responseXML);
				
				setInnerHTML("optionsHeadings", "<td colspan=0>Users</td>");
				var inner = "<td class='optionsAction'>";
				for(var i = 0; i < users.length; i++) {
					if(i%5 == 0 && i != 0) {
						inner += "</td><td class='optionsAction'>";
					}
					inner += "<span class='schOption' onclick='pAssignShift(" + day + ", " + id + ", \"" + users[i].split(":")[0] + "\");'>" + users[i].split(":")[1] + "</span><br>";
				}
				inner += "</td>";
				setInnerHTML("optionsValues", inner);
			}
			else {
				setInnerHTML("shift" + id, "Error Getting Users");
			}
		}
			
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}
	
function pAssignShift(day, id, user) {
	if(controlsLocked)
		return;
	// first calc which row it'll be in.
	var row = day - dayIndex;
	
	// okay, now send the request.
	lockControls();
	var url = root +"/ScheduleResponder?action=pAssign&day=" + day + "&id=" + id + "&new=" + user;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				// var response = xmlHttp.responseXML;
				getShiftRow(day, row);
			}
			else {
				setInnerHTML("shift" + id, "ERROR");
			}
		}
			
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}
// ------------------------------------------------------------------------------------------------------------------------------------------------
// End Of Schedule Functions
// ------------------------------------------------------------------------------------------------------------------------------------------------



// ************************************************************************************************************************************************
// ************************************************************************************************************************************************
// Start Of Administration Functions
// ************************************************************************************************************************************************
// ************************************************************************************************************************************************
function adminGetUsers(){
	var url = root +"/AdministrationResponder?action=getUsers";
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				adminParseUsersForWorkforceManagement(xmlHttp.responseXML);
			}
			else {
				setInnerHTML("adminProposedWorkforce", "Error Getting Users");
				setInnerHTML("adminAllStudents", "Error Getting Users");
			}
		}
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function adminParseUsersForWorkforceManagement(responseXML){
	var response = responseXML.getElementsByTagName("result")[0];
	var htmlUsersCurrentlyInJob = "";
	var htmlUsersCurrentlyNotInJob = "";
	for (var i = 0; i < response.childNodes.length; i++) {
		var user = response.childNodes[i];
		var username = user.childNodes[0].textContent;
		var usersFirstLastNames= user.childNodes[1].textContent;
		var status	= user.childNodes[2].textContent;
		if (status=="employed"){
			htmlUsersCurrentlyInJob += "<option value='"+username+":"+status+"' > "+usersFirstLastNames+"</option>";
		} else if (status=="unemployed"){
			htmlUsersCurrentlyNotInJob += "<option value='"+username+":"+status+"' > "+usersFirstLastNames+"</option>";
		}
	}
	setInnerHTML("adminProposedWorkforce",htmlUsersCurrentlyInJob);
	setInnerHTML("adminAllStudents",htmlUsersCurrentlyNotInJob);
}

function adminAddStudent(){
	var proposedWorkforce = $("adminProposedWorkforce");
	var allStudents = $("adminAllStudents");
	var j = 0;
	var studentsToAdd = new Array();
	for(var i = 0; i < allStudents.options.length; i++){
		if (allStudents.options[i].selected){
			studentsToAdd[j] = allStudents[i];
			j++;
		}
	}
	for(var k = 0; k < j; k++){
		studentToAdd =  studentsToAdd[k];
		allStudents.remove[studentToAdd.index];
		proposedWorkforce.add(studentToAdd, null);
	}
}

function adminRemoveStudent(){
	var proposedWorkforce = $("adminProposedWorkforce");
	var allStudents = $("adminAllStudents");
	var j = 0;
	var studentsToRemove = new Array();
	for(var i = 0; i < proposedWorkforce.options.length; i++){
		if (proposedWorkforce.options[i].selected){
			studentsToRemove[j] = proposedWorkforce[i];
			j++;
		}
	}
	for(var k = 0; k < j; k++){
		studentToRemove =  studentsToRemove[k];
		proposedWorkforce.remove[studentToRemove.index];
		allStudents.add(studentToRemove, null);
	}
}

function adminSaveUpdatedWorkforce(){
	var proposedWorkforce = $("adminProposedWorkforce");
	var allEmployees = $("adminAllStudents");
	var employeesToRemove = "";
	var employeesToAdd = "";
	var employeesHaveBeenAdded = false;
	var employeesHaveBeenRemoved = false;
	for (var i = 0; i < proposedWorkforce.options.length; i ++){
		if(proposedWorkforce.options[i].value.split(":")[1] == "unemployed"){
			employeesToAdd += proposedWorkforce.options[i].value.split(":")[0] + ":";
			employeesHaveBeenAdded = true;
		}
	}
	for (var i = 0; i < allEmployees.options.length; i ++){
		if(allEmployees.options[i].value.split(":")[1] == "employed"){
			employeesToRemove += allEmployees.options[i].value.split(":")[0] + ":";
			employeesHaveBeenRemoved = true;
		}
	}
	if (employeesHaveBeenAdded || employeesHaveBeenRemoved){
		adminAjaxSaveUpdatedWorkforce(employeesToRemove, employeesToAdd, employeesHaveBeenAdded, employeesHaveBeenRemoved);
	}
}

function adminAjaxSaveUpdatedWorkforce(employeesToRemove, employeesToAdd, employeesHaveBeenAdded, employeesHaveBeenRemoved){
	var urlAddPart = "";
	var urlMiddlePart = "";
	var urlRemovePart = "";
	if (employeesHaveBeenAdded){
		urlAddPart = "employeesToAdd="+employeesToAdd;
	}
	if (employeesHaveBeenAdded && employeesHaveBeenRemoved){
		urlMiddlePart = "&";
	}
	if (employeesHaveBeenRemoved){
		urlRemovePart = "employeesToRemove="+employeesToRemove;
	}

	var url = root +"/AdministrationResponder?action=saveUpdatedWorkforce&" +urlAddPart+urlMiddlePart+urlRemovePart;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				alert("sEMP has successfully saved your updated workforce.");
				adminGetUsers();
			}
			else {
				alert("Error: Internal server error. Ajax call to save users failed.");
				adminGetUsers();
			}
		}
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

// ------------------------------------------------------------------------------------------------------------------------------------------------
// End Of Administration Functions
// ------------------------------------------------------------------------------------------------------------------------------------------------



//************************************************************************************************************************************************
//************************************************************************************************************************************************
//Start Of Mail Room Functions
//************************************************************************************************************************************************
//************************************************************************************************************************************************
function mailRoomGetUsers() {
	var url = root + "/MailRoomResponder?action=searchForStudent&searchString="
			+ $('mailRoomSearchParameters').value;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == 4) {
			if (xmlHttp.status == 200) {
				mailRoomParseUsersForLookUp(xmlHttp.responseXML);
			} else {
				setInnerHTML("mailRoomStudentsMatching", "Error Getting Users");
			}
		}
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function mailRoomParseUsersForLookUp(responseXML) {
	var response = responseXML.getElementsByTagName("result")[0];
	var mailRoomStudentsMatchingHTML = "<table width=\"360\" border=\"2\" cellpadding=\"1\"	align=\"center\">";
	for ( var i = 0; i < response.childNodes.length; i++) {
		var user = response.childNodes[i];
		var firstName = user.childNodes[0].textContent;
		var lastName = user.childNodes[1].textContent;
		var mailboxNumber = user.childNodes[2].textContent;
		var id = user.childNodes[3].textContent;
		var row = "<tr><td width=\"120\">"
				+ firstName
				+ " "
				+ lastName
				+ "</td><td width=\"120\">"
				+ mailboxNumber
				+ "</td>"
				+ "<td width=\"120\">	<input type=\"button\" class=\"smallMaroonButton\" value=\"Record & Email\" id=\"mailroomSendEmailButton"
				+ id + "\" onclick=\"mailRoomRecordAndEmail(" + id + ")\">"
				+ "</td>	</tr>";
		mailRoomStudentsMatchingHTML += row;
	}
	mailRoomStudentsMatchingHTML += "</table>";
	setInnerHTML("mailRoomStudentsMatching", mailRoomStudentsMatchingHTML);
}

function mailRoomSearchPackages() {
	var url = root	+ "/MailRoomResponder?action=searchForPackages&searchString="
			+ $('mailRoomPackageSearchParameters').value + "&searchType="	+ $('searchType').value;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == 4) {
			if (xmlHttp.status == 200) {
				mailRoomParsePackagesForSearch(xmlHttp.responseXML);
			} else {
				setInnerHTML("mailRoomPackagesMatching",
						"Error Searching Packages");
			}
		}
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

function mailRoomParsePackagesForSearch(responseXML) {
	var response = responseXML.getElementsByTagName("result")[0];
	var mailRoomPackagesMatchingHTML = "<table width=\"800\" border=\"2\" cellpadding=\"1\" align=\"center\">";
	for ( var i = 0; i < response.childNodes.length; i++) {
		var matchingPackage = response.childNodes[i];
		var Package_ID = matchingPackage.childNodes[0].textContent;
		var Date = matchingPackage.childNodes[1].textContent;
		var Box_Number = matchingPackage.childNodes[2].textContent;
		var First_Name = matchingPackage.childNodes[3].textContent;
		var Last_Name = matchingPackage.childNodes[4].textContent;
		var Shipper = matchingPackage.childNodes[5].textContent;
		var Package_Type = matchingPackage.childNodes[6].textContent;
		var Color = matchingPackage.childNodes[7].textContent;
		var Location = matchingPackage.childNodes[8].textContent;
		var Employee = matchingPackage.childNodes[9].textContent;

		var row = "<tr><td width=\"50\">" + Package_ID
				+ "</td><td width=\"50\">" + Date + "</td><td width=\"50\">"
				+ Box_Number + "</td><td width=\"50\">" + First_Name
				+ "</td><td width=\"50\">" + Last_Name
				+ "</td><td width=\"50\">" + Shipper + "</td><td width=\"50\">"
				+ Package_Type + "</td><td width=\"50\">" + Color
				+ "</td><td width=\"50\">" + Location
				+ "</td><td width= \"50\">" + Employee + "</td></tr>";
		mailRoomPackagesMatchingHTML += row;
	}
	mailRoomPackagesMatchingHTML += "</table>";
	setInnerHTML("mailRoomPackagesMatching", mailRoomPackagesMatchingHTML);
}

function mailRoomRecordAndEmail(id) {
	var shipper = $("ShipperSelector").value;
	var packageType = $("PackageTypeSelector").value;
	var color = $("ColorSelector").value;
	var location = $("LocationSelector").value;
	var url = root + "/MailRoomResponder?action=recordAndEmail&ID=" + id
			+ "&shipper=" + shipper + "&packageType=" + packageType + "&color="
			+ color + "&location=" + location;
	var xmlHttp = GetXmlHttpObject();
	xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == 4) {
			if (xmlHttp.status == 200) {
				document.getElementById("mailroomSendEmailButton" + id).value = "Recorded & Sent!";
				document.getElementById("mailroomSendEmailButton" + id).style.backgroundColor = '#4D4D4D';
				var response = xmlHttp.response; //added semicolon

				var packageSlipURL = "/MailRoom?action=PackageSlip&packageID="
						+ response;
				window.open(packageSlipURL, '_blank');

			} else {
				setInnerHTML("mailroomSendEmail" + xmlHttp.responseXML,
						"Error Sending Email or Recording");
			}
		}
	};
	xmlHttp.open("POST", url, true);
	xmlHttp.send(null);
}

//------------------------------------------------------------------------------------------------------------------------------------------------
//End Of Mail Room Functions
//------------------------------------------------------------------------------------------------------------------------------------------------

//************************************************************************************************************************************************
//************************************************************************************************************************************************
//Start Of LTA Check in Functions
//************************************************************************************************************************************************
//******************************************************************************************************* *****************************************
var LTACheckInMapList = new Array('poppa','ktc','south','rrl');

function LTACheckInMapRotator (x){
	if (isGate || isSchedule) {
		isMapRotator = false;
	}
	if(isMapRotator){
		 hideMap(LTACheckInMapList[x]+'Map');
		 x=x+1;
		 x=x%4;
		 showMap(LTACheckInMapList[x]);
		 setTimeout("LTACheckInMapRotator("+x+")",5000);
	}
}
//------------------------------------------------------------------------------------------------------------------------------------------------
//Start Of LTA Check in Functions
//------------------------------------------------------------------------------------------------------------------------------------------------

