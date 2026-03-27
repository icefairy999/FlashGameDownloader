//我们把4399的h5api重定向到这里，把函数改一改，基本上就是只改了广告播放相关，别的我也不会改
window.h5api = {
	initGame: function(){
		console.warn("试图调用api: initGame");
	},
	/**
	 * 设置进度条进度
	 * @param {int} num 范围1~100，进度值
	 */
	progress: function (num) {
		console.warn("试图调用api: progress");
	},
	/**
	 * 提交分数
	 * @param {int} score 分数
	 * @param {func} callback 回调函数
	 */
	submitScore: function (score, callback) {
		console.warn("试图调用api: submitScore");
	},
	/**
	 * 获得排行榜
	 * @param {func} callback 回调函数
	 */
	getRank: function (callback) {
		console.warn("试图调用api: getRank");
	},
	/**
	 * 是否能播放广告
	 * @param {func} callback 回调函数
	 * @returns {boolean} 是否能播放广告
	 */
	canPlayAd: function (callback) {
		console.log("调用api: canPlayAd");
		if(callback){
			callback({canPlayAd:true});
		}
		return true;
	},
	/**
	 * 播放广告
	 * @param {func} callback 回调函数
	 */
	playAd: function (callback) {
		console.log("调用api: playAd")
		callback({code:10000,message:"开始播放"});
		callback({code:10001,message:"播放结束"});
	},
	/**
	 * 播放优量汇广告(仅供测试)
	 * @param {String} placementId 广告位Id
	 * @param {func} callback 回调函数
	 */
	playYlhAd: function (placementId, callback) {
		//我不知他在搞什么
		console.warn("试图调用api: playYlhAd");
		console.log("调用api: playYlhAd, placementId:", placementId);
		if (callback) {
			callback({code: 10000, message: "开始播放"});
			callback({code: 10001, message: "播放结束"});
		}
	},
	/**
	 * 播放插屏广告
	 */
	playInterstitialAd: function () {
		console.warn("试图调用api: playInterstitialAd");
		//它没有回调函数，这更让人摸不着头脑了
	},
	/**
	 * 调用分享功能
	 */
	share: function () {
		console.warn("试图调用api: share");
	},
	/**
	 * 获得用户当前是否登录
	 */
	isLogin: function () {
		console.log("调用api: isLogin");
		return false;
	},
	/**
	 * 用户登录
	 * @param {func} callback 回调函数
	 */
	login: function (callback) {
		console.warn("试图调用api: login");
	},
	/**
	 * 获得用户头像地址，高宽为120*120像素
	 *
	 * @param {String} uid 用户编号
	 * @param {String} size 头像大小
	 * @return 用户头像地址
	 */
	getUserAvatar: function (uid, size) {
		console.warn("试图调用api: getUserAvatar");
	},
	/**
	 * 获得用户小头像地址，高宽为48*48像素（small 不再使用，统一调整为 middle）
	 */
	getUserSmallAvatar: function (uid) {
		console.warn("试图调用api: getUserSmallAvatar");
	},
	/**
	 * 获得用户大头像地址，高宽为200*200像素
	 */
	getUserBigAvatar: function (uid) {
		console.warn("试图调用api: getUserBigAvatar");
	},
	/**
	 * 获得用户超大头像地址，高宽为360*360像素
	 */
	getUserLargeAvatar: function (uid) {
		console.warn("试图调用api: getUserLargeAvatar");
	},
	/**
	 * 提交排名
	 *
	 * @param {int} score 分数
	 * @param {func} callback 回调函数
	 */
	submitRanking: function (score, callback) {
		console.warn("试图调用api: submitRanking");
	},
	/**
	 * 新版提交排名
	 * @param {*} rankId 排行榜id
	 * @param {*} score 分数
	 * @param {*} callback 回调函数
	 */
	submitRankScore: function (rankId, score, callback) {
		console.warn("试图调用api: submitRankScore");
	},
	/**
	 * 获得我的排名
	 *
	 * @param {func} callback 回调函数
	 */
	getMyRanking: function (callback) {
		console.warn("试图调用api: getMyRanking");
	},
	/**
	 * 获得排名列表
	 *
	 * @param {func} callback 回调函数
	 * @param {int} page 页码 从1开始
	 * @param {int} step 每页条数
	 */
	getRanking: function (callback, page, step) {
		console.warn("试图调用api: getRanking");
	},
	/**
	 * 展示排行榜列表面板
	 */
	showRanking: function () {
		console.warn("试图调用api: showRanking");
	},
	/**
	 * 展示新版排行榜面板
	 */
	showRankList: function () {
		console.warn("试图调用api: showRankList");
	},
	/**
	 * 获得我附近排名列表
	 *
	 * @param {func} callback 回调函数
	 * @param {int} step 需要条数
	 */
	getNearRanking: function (callback, step) {
		console.warn("试图调用api: getNearRanking");
	},
	/**
	 * 敏感词检查
	 *
	 * @param {*} word
	 * @param {*} callback
	 */
	checkWord: function (word, callback) {
		console.warn("试图调用api: checkWord");
	},
	/*
	 * 展示推荐面板
	 */
	showRecommend: function () {
		console.warn("试图调用api: showRecommend");
	},
	/**
	 * 存档
	 * @param {*} params.more 是否是多档 true | false
	 * @param {*} params.type 操作类型 write | read
	 * @param {*} params.title 存档标题 type为write时必填
	 * @param {*} params.data 存档数据 type为write时必填
	 * @param {*} params.callback 回调函数
	 */
	save: function (params) {
		console.warn("试图调用api: save");
	},
	/**
	 * 游戏模式
	 * @param {*} mode 1 游客 2 账户，不传则打开面板
	 */
	gameMode: function (mode) {
		console.warn("试图调用api: gameMode");
	},
	/**
	 * 显示引导面板
	 * @param {*} callback 领取按钮回调
	 */
	showGuide: function (callback, index) {
		console.warn("试图调用api: showGuide");
	},
	/**
	 * 检查API是否能使用
	 */
	checkAPI: function () {
		console.warn('正在使用我自己的替代api，许多功能将无法使用');
	}
};
window.h5api.checkAPI();
