// check for display="none" style
$('g').each(function(){
	if( this.style.display == 'none'){
		console.log("this: ", this)
		this.remove()
	}
});

$('g[display=none]').each(function(){
	console.log("this: ", this)
	this.remove()
});

// check if does not have children
ids = ['compass', 'gridOverlay', 'terrs', 'biomes', 'cells', 
		'coordinates', 'cults', 'temperature', 'rural', 'urban',
		'towns', 'cities']

$('g').each(function(){
	if(ids.includes(this.id)){
		if(this.children.length == 0){
			// general
			console.log("this: ", this)
			this.remove()
			// population
			if(this.id == 'rural' || this.id == 'urban'){
				console.log('g[id=population]')
				$('g[id=population]').remove()
			}
			// burg labels
			if(this.id == 'towns' || this.id == 'cities'){
				console.log('g[id=burgLabels]')
				$('g[id=population]').remove()
			}
		}
	}
});