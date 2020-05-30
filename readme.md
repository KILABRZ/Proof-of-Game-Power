## Proof of Game Power

* 透過以遊戲作為運算難題，來做成流量控管的實驗。

### 架構

* 需要 demo 用的 Client, Server，以及最重要的 Game Page
* Client 用 script 達成 Flash Crowd 的 demo。
* Server 要實作一個 Service，並且要能驗證 Game Record 的 Proof。
* Game Page 必須是靜態的，可以控制難度，並且要能夠隱藏 Token。

### 雜記

* Server 拿 Flask 架
* Game Page 最後應該會長成這個樣子：
  * <code>def generateGamePage(expected_pass_time, token):<br>	...... <br>	return javascript</code>





