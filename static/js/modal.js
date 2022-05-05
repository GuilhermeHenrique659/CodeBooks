$('#modal_fin').on('hide.bs.modal', function (event) {
    document.getElementById('porcentagem_corr').value= null;
    document.getElementById('porcentagem_imob').value= null;
    document.getElementById('valor_corr').value= null;
    document.getElementById('valor_imob').value= null;
})

$('#modal_fin').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget)
    var id = button.data('id')
    var total = button.data('total')
    var corretor = button.data('corretor')
    var modal = $(this)
    modal.find('.modal-title').text('Insira os valores para o registro: ' + id)
    modal.find('#id_fin').val(id)
    modal.find('#total').val(total)
    modal.find('#corretor').val(corretor)

})