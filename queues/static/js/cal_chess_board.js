window.onload = function () {
    // 通过皇后的数量，计算棋盘的总大小
    var title = document.getElementsByClassName("title")[0].innerText
    var chessBoard = document.getElementsByClassName("chess_board")[0]
    console.log(title)
    console.log(chessBoard)
    num = this.parseInt(title)
    chessBoard.style.width = num * 70 + "px" 
    chessBoard.style.height = num * 70 + "px"
}