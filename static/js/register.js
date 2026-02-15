function showToast(message) {
   const toast = document.getElementById('toast');
   toast.textContent = message;
   toast.classList.add('show');

   setTimeout(() => {
       toast.classList.remove('show');
   }, 5000); // Toast disappears after 3 seconds
}


   console.log("js is working");
   const nextBtn = document.querySelector('.next-btn');
   const createAccountBtn = document.querySelector('.create-account-btn');
   const steps = document.querySelectorAll('.form-step');
   const progress = document.querySelector('.progress-bar-inner');

   let currentStep = 0; // Track the current step

   window.onload = function (){
    console.log("Next button pressed");
    // Hide current step and move to the next step
    steps[currentStep].classList.remove('form-step-active');
    currentStep = 1;

    // Show the next step
    steps[currentStep].classList.add('form-step-active');

    // Update progress bar
    if(progress){
    const progressPercentage = 100;
    progress.style.width = progressPercentage + '%';
    const border = document.querySelector('#step2-circle');
    const bordervalue = document.querySelector('#bordervalue');
    border.style.borderColor = '#DE235B';
    border.style.color = '#DE235B';
    console.log(bordervalue.innerHTML); 
    bordervalue.style.color = '#DE235B';
    }
   }

//    nextBtn.addEventListener('click', function () {
//    console.log("Next button pressed");
//     // Hide current step and move to the next step
//     steps[currentStep].classList.remove('form-step-active');
//     currentStep = 1;

//     // Show the next step
//     steps[currentStep].classList.add('form-step-active');

//     // Update progress bar
//     if(progress){
//     const progressPercentage = 100;
//     progress.style.width = progressPercentage + '%';
//     const border = document.querySelector('#step2-circle');
//     const bordervalue = document.querySelector('#bordervalue');
//     border.style.borderColor = '#DE235B';
//     border.style.color = '#DE235B';
//     console.log(bordervalue.innerHTML); 
//     bordervalue.style.color = '#DE235B';

//     }

//     createAccountBtn.addEventListener('click' ,function (){

//         steps[currentStep].classList.remove('form-step-active');
//         currentStep = 0;
//         steps[currentStep].classList.add('form-step-active');
//         nextBtn.style.display = 'block'; // Hide "Next" button
//         createAccountBtn.style.display = 'none'; // Show "Create Account" button
//         if(progress){
//             const progressPercentage = 0;
//             progress.style.width = progressPercentage + '%';
//             const border = document.querySelector('#step2-circle');
//             const bordervalue = document.querySelector('#bordervalue');
//             border.style.borderColor = 'var(--Overlay-stroke, #C1C7CD)';
//             border.style.color = 'var(--Overlay-stroke, #C1C7CD)';
//             console.log(bordervalue.innerHTML); 
//             bordervalue.style.color = 'var(--Overlay-stroke, #C1C7CD)';
        
//             }



//     })



//     // Check if it's the last step
//     if (currentStep == 1) {
//         nextBtn.style.display = 'none'; // Hide "Next" button
//         createAccountBtn.style.display = 'block'; // Show "Create Account" button
//     }
// });