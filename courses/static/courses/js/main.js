var csrftoken = "";

/** Filter the list of courses by category
	@category - Clicked categoty
 */
 function filterCourses(category) {

	// Update category name at the top of page
	document.querySelector("#Categories").innerHTML = category.getAttribute('data-categoryname');

	// Highlight Category
	document.querySelectorAll('[data-selector="category-entry"]').forEach ( categorycard => {
		categorycard.classList.remove("display-5");
	});
	category.classList.add('display-5')

	// Get category id
	var id = category.getAttribute('data-categoryid');
	document.querySelectorAll('[data-selector="course-entry"]').forEach ( course => {
		if (id==0) // Show courses for "All Categories" => ALL
			course.classList.remove("d-none");
		else { // Show courses for a specific category id
			let catlist = course.getAttribute('data-categories').replace(/[\[|\]]/g,"").split(",");
			if (catlist.includes(id))
				course.classList.remove("d-none");
			else
				course.classList.add("d-none");
		}
	}); 
} // End filterCourses

function getAddsInfo (courseid) {
	// Get complete adds list for course
	let addsList = document.querySelectorAll('input'+`.check-${courseid}`+'[type="checkbox"]');
	/* Get number of selected (checked) course adds (all checked -checkboxes- of a given class)
	   And calculate price */
	var freeAdds = 0; // Num if free adss
	var extrapriceAdds = 0;
	addsList.forEach( add => { 
		if (add.checked) {
			if (add.getAttribute('data-free').toLowerCase() == 'true')
				freeAdds++;
			else
				extrapriceAdds += parseFloat(add.getAttribute('data-extraprice'));
		}
	});
	response = {"list": addsList, 
				"numberfree": freeAdds, 
				"extraprice": extrapriceAdds }
	return response;
} // End getAddsInfo

function updateOrderCoursePrice (courseid) {
    let cprice = parseFloat(document.querySelector(`#modal-${courseid}-coursePrice`).getAttribute('value'));
	let adds = getAddsInfo (courseid); // Get adds complete info, including total extraprices 
    totalPrice = cprice + adds.extraprice;
    document.querySelector(`#modal-${courseid}-coursePrice`).innerHTML = totalPrice.toFixed(2);
    return adds;
} // End updateOrderCoursePrice

/** EVENT HANDLER - When selected course Adds check
	Control number of free adds and calculate price
	@add - checked add
*/
function checkOrderAdds (courseid) {
	// Get max number of free adds allowed
	let maxAdds = document.querySelector(`#modal-${courseid}-courseAdds`).getAttribute('value');

	// Update course price and get adds list, and num of free adds selected
	let adds = updateOrderCoursePrice (courseid);
	let addsList = adds.list;
	let numAdds = adds.numberfree;
	
	// Update nmumber of free adds available to select
	document.querySelector(`#modal-${courseid}-courseAdds`).innerHTML = `${maxAdds-numAdds}`;

	if (numAdds == maxAdds) { // Disable rest of free adds checkboxes
		addsList.forEach ( add => {	
			if (!add.checked && add.getAttribute('data-free').toLowerCase() == 'true')
				add.disabled = true; 
		}); 
	} else if (numAdds < maxAdds) { // Enable all disabled items
		addsList.forEach ( add => {	if (add.disabled) add.disabled = false; }); 
	}
} // End checkOrderAdds

/** When load page */
document.addEventListener('DOMContentLoaded', load);
/** Load
 * - Set "onclick" event handlers for ...
 * - Set "change"  event handlers for ...
 */
function load () {

	/** Click event handler for click card-link Category link
	  */
	document.querySelectorAll('[data-selector="category-entry"]').forEach ( category => {
		category.addEventListener('click', event => { filterCourses(category) });
	}); // End .plusButton'.onclick

	/** Click event handler for course Adds Changes
		Update Adds limits and price in modal dialog */
	document.querySelectorAll("input[type='checkbox']").forEach ( add => {
		add.addEventListener('change', event => { 
			// Check adds for course
			checkOrderAdds(add.getAttribute('data-courseid'));
		});
	}); // End course Adds Changes

	csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
} // End load
