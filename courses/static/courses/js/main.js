var csrftoken = "";


/** SET Intersection
	Return the intersection between 2 sets
 */
function setIntersection(set1, set2) {
	return new Set(Array.from(set1).filter(x => set2.has(x)))	
}


/** Filter the list of courses by category
	@category - Clicked categoty
 */
 function filterCourses(category) {
	// Get category id clicked element
	var id = category.getAttribute('data-categoryid');
 	// Manage clicked checkboxes according to "All Courses" (id === '0')
 	var checkboxes = document.querySelectorAll("input[name='courseCategories']");
 	if (id === '0') {
 		let checked = category.checked;
 		// Update all checkboxes according to All Categories id === '0'
		for (var i = 1; i < checkboxes.length; i++)
			checkboxes[i].checked = checked;
 	} else {
		if (!category.checked)
	 		// If any of the other checboxes is uncheked, "ALL Categories" (Categories id === '0') must be uncheked 
			checkboxes[0].checked = false;
		else {
			// If all the categories, except 0, are checked, ALL must be checked
			let count = 0;
			for (var i = 1; i < checkboxes.length; i++)
				if (checkboxes[i].checked)
					count++;
			if (count == checkboxes.length-1)
				checkboxes[0].checked = true;
		}
 	}
 	// Make a SET of checked values (categories), except "ALL"
	var filterCategories = new Set();
	var checkboxes = document.querySelectorAll("input[name='courseCategories']:checked")
	for (var i = 0; i < checkboxes.length; i++)
		filterCategories.add(checkboxes[i].value);

	// Set visible only courses with
	document.querySelectorAll('[data-selector="course-entry"]').forEach ( course => {
		if (id==0) 
			if (category.checked)
			// Show courses for "All Categories" => ALL				
				course.classList.remove("d-none");
			else
				course.classList.add("d-none");
		else { // Show courses for a specific set of señected categories
			let courseCategorySet = new Set (course.getAttribute('data-categories').replace(/[\[|\]]/g,"").split(","));
			// If the is an intersection between course categories and selected categories, they must be displayed
			if (setIntersection(courseCategorySet, filterCategories).size > 0)
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
	document.querySelectorAll("input[name='courseCategories']").forEach ( category => {
		category.addEventListener('click', event => { 
			filterCourses(category) 
		});
	}); // End .plusButton'.onclick

	/** Click event handler for course Adds Changes
		Update Adds limits and price in modal dialog */
	document.querySelectorAll("input[name='courseAdds']").forEach ( add => {
		add.addEventListener('change', event => { 
			checkOrderAdds(add.getAttribute('data-courseid'));// Check adds for course
		});
	}); // End course Adds Changes

	csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
} // End load
