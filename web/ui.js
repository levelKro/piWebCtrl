ga = [];
function getApi(id,action,values) { 
	if(!values) values="?tm"+Math.random();
	else values=values+"&tm"+Math.random();
	pass = document.getElementById("password").value;
	if(pass != ""){
		document.getElementById(id).innerHTML="";
		values = values + "&pass=" + pass;
		if (window.XMLHttpRequest) { ga[id]=new XMLHttpRequest(); }
		else { ga[id]=new ActiveXObject("Microsoft.XMLHTTP"); }
		ga[id].onreadystatechange=function() {
			if (ga[id].readyState==4 && ga[id].status==200) {
				var result=ga[id].responseText;		
				var values=JSON.parse(result);	
				if(!values.error){
					if(values.html) {
						document.getElementById(id).innerHTML=values.html;
					}
					if(values.cmd){
						for(var c=0;c<values.cmd.length;c++){
							console.log("Eval: "+values.cmd[c]);
							eval(values.cmd[c]);
						}
					}
					
				}
				else{
					document.getElementById(id).innerHTML=values.error;
				}	
			}
		}
		ga[id].open("GET",action+values,true);
		ga[id].send();	
	
	}
	else {
		document.getElementById(id).innerHTML="Password can't be empty"
	}		
}

function geStats(id) { 
	if (window.XMLHttpRequest) { gStats=new XMLHttpRequest(); }
	else { gStats=new ActiveXObject("Microsoft.XMLHTTP"); }
	gStats.onreadystatechange=function() {
		if (gStats.readyState==4 && gStats.status==200) {
			var result=gStats.responseText;		
			var values=JSON.parse(result);	
			if(!values.error){
				document.getElementById("statsCPUSpeed").innerHTML=values.cpuspeed;
				document.getElementById("statsCPUTemp").innerHTML=values.cputemp;
				document.getElementById("statsRAMFree").innerHTML=values.ramfree;
				document.getElementById("statsRAMTotal").innerHTML=values.ramtotal;
				document.getElementById("statsSYSLoad").innerHTML=values.load;
				document.getElementById("statsSYSUptime").innerHTML=values.uptime;
				document.getElementById("statsSYSIP").innerHTML=values.ip;
			}
			else{
				document.getElementById(id).innerHTML=values.error;
			}	
		}
	}
	gStats.open("GET","stats.json?"+Math.random(),true);
	gStats.send();	
}

 setTimeout("geStats('output')",2000);