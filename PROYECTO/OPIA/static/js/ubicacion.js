// Step 1: Get user coordinates 
var mostrar_region;

const regiones = {
    "Región de Arica y Parinacota": 1,
    "Región de Tarapacá": 2,
    "Región de Antofagasta": 3,
    "Región de Atacama": 4,
    "Región de Coquimbo": 5,
    "Región de Valparaíso": 6,
    "Región del Libertador General Bernardo O'Higgins": 8,
    "Región de Maule": 9,
    "Región de Ñuble": 10,
    "Región del Biobío": 11,
    "Región de La Araucanía": 12,
    "Región de Los Ríos": 13,
    "Región de Los Lagos": 14,
    "Región de Aysén del General Carlos Ibáñez del Campo": 15,
    "Región de Magallanes y de la Antártica Chilena": 16,
    "Región Metropolitana de Santiago": 7
};

function getCoordintes() { 
	var options = { 
		enableHighAccuracy: true, 
		timeout: 5000, 
		maximumAge: 0 
	}; 

	function success(pos) { 
		var crd = pos.coords; 
		var lat = crd.latitude.toString(); 
		var lng = crd.longitude.toString(); 
		var coordinates = [lat, lng]; 
		getCity(coordinates); 
		return; 

	} 

	function error(err) { 
		console.warn(`ERROR(${err.code}): ${err.message}`); 
	} 

	navigator.geolocation.getCurrentPosition(success, error, options); 
} 

// Step 2: Get city name 
function getCity(coordinates) { 
	var xhr = new XMLHttpRequest(); 
	var lat = coordinates[0]; 
	var lng = coordinates[1]; 

	// Paste your LocationIQ token below. 
	xhr.open('GET', " https://us1.locationiq.com/v1/reverse.php?key=pk.a73d396d2124f81921446f0ee1a967b5&lat=" + 
	lat + "&lon=" + lng + "&format=json", true); 
	xhr.send(); 
	xhr.onreadystatechange = processRequest; 
	xhr.addEventListener("readystatechange", processRequest, false); 

	function processRequest(e) { 
        try{
          if (xhr.readyState == 4 && xhr.status == 200) { 
			var response = JSON.parse(xhr.responseText); 
			var state = response.address.state;
            mostrar_region = state; 
			return; 
		}  
        }finally{
            console.log(mostrar_region);
			var value = regiones[mostrar_region] ;
			console.log(value);
            //aca ya esta actualizado del valor
        }
		   
	} 
} 




