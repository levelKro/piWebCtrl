ga = [];
function getApi(id,action,values) { 
	if(!values) values="?tm"+Math.random();
	else values=values+"&tm"+Math.random();
	if (window.XMLHttpRequest) { ga[id]=new XMLHttpRequest(); }
	else { ga[id]=new ActiveXObject("Microsoft.XMLHTTP"); }
	ga[id].onreadystatechange=function() {
		if (ga[id].readyState==4 && ga[id].status==200) {
			//document.getElementById(id).innerHTML=ga[id].responseText;
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