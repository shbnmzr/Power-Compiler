const codeArea = document.getElementById('code-area');
const consoleWindow = document.querySelector('.console');
const codeWindow = document.querySelector('.code-editor');
const link = document.getElementById('save-button');
const backdrop = document.querySelector('.backdrop');
const modal = document.querySelector('.modal');
const optionsWindow = document.querySelector('.options-container');
const newFile = document.getElementById('new-file');
const positiveOption = document.getElementById('positive');
const negativeOption = document.getElementById('negative');
const operators = ['Jam', 'Kam', 'Zarb', 'Tagsim', 'Bagimande', '&B',
    '&BM', '&K', '&KM', '&MM', '&NM', 'Va', 'Ya'];
const keywords = ['Main', 'agar', 'ta', 'Benevis', 'Begir', 'Bemir'];

negativeOption.addEventListener('click', closeModal, false);
backdrop.addEventListener('click', closeModal);

$(function() {
    $('#code-area').numberedtextarea({
        height: '100%'
    });
})

link.addEventListener('click', function () {
    backdrop.classList.add('open');
    modal.classList.add('open');
   
    
}, false);

newFile.addEventListener('click', function () {
    backdrop.classList.add('open');
    optionsWindow.classList.add('open');
}, false);

positiveOption.addEventListener('click', function () {
    optionsWindow.classList.remove('open');
    modal.classList.add('open');
}, false);

function closeModal() {
    backdrop.classList.remove('open');
    modal.classList.remove('open');
    optionsWindow.classList.remove('open');
    name.value = '';
}