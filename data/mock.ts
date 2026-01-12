import { Book, Vocabulary } from "@/types";

/**
 * 模拟词汇数据
 * 包含真实的雅思核心单词及其完整信息
 */
export const mockVocabularies: Record<string, Vocabulary> = {
  ambitious: {
    word: "ambitious",
    meaning: "有野心的，雄心勃勃的",
    phonetic: "/æmˈbɪʃəs/",
    root: "ambit- (around) + -ious (形容词后缀)",
    example: "She has ambitious plans to start her own business.",
    exampleCn: "她有雄心勃勃的计划要创办自己的公司。",
  },
  meticulous: {
    word: "meticulous",
    meaning: "一丝不苟的，极其仔细的",
    phonetic: "/məˈtɪkjələs/",
    root: "metic- (fear) + -ulous (充满...的)",
    example: "He is meticulous about every detail in his work.",
    exampleCn: "他对工作中的每一个细节都一丝不苟。",
  },
  prestigious: {
    word: "prestigious",
    meaning: "有声望的，享有盛誉的",
    phonetic: "/preˈstɪdʒəs/",
    root: "prestig- (illusion, prestige) + -ious",
    example: "She graduated from a prestigious university.",
    exampleCn: "她毕业于一所享有盛誉的大学。",
  },
  sophisticated: {
    word: "sophisticated",
    meaning: "复杂的，精密的；世故的",
    phonetic: "/səˈfɪstɪkeɪtɪd/",
    root: "soph- (wisdom) + -isticated",
    example: "The company uses sophisticated technology.",
    exampleCn: "这家公司使用精密的技术。",
  },
  resilient: {
    word: "resilient",
    meaning: "有弹性的，能恢复的；坚韧的",
    phonetic: "/rɪˈzɪliənt/",
    root: "re- (back) + salire (to jump)",
    example: "Children are often more resilient than adults.",
    exampleCn: "孩子们往往比成年人更有韧性。",
  },
  elaborate: {
    word: "elaborate",
    meaning: "精心制作的，详尽的",
    phonetic: "/ɪˈlæbərət/",
    root: "e- (out) + labor (work)",
    example: "They made elaborate preparations for the event.",
    exampleCn: "他们为这次活动做了精心的准备。",
  },
};

/**
 * 模拟书籍数据
 * 《顶级豪门的继承人》- 包含2个章节的完整小说数据
 */
export const mockBook: Book = {
  id: "book-001",
  title: "顶级豪门的继承人",
  author: "流年",
  coverColor: "#8B5CF6", // 紫色主题
  chapters: [
    {
      id: "chapter-001",
      title: "第一章：命运的转折",
      content: `林晚晚站在那扇厚重的红木门前，深吸了一口气。这是她第一次踏进这座位于市中心的顶级豪宅。

门缓缓打开，映入眼帘的是 {elaborate|精心制作的} 装饰和 {sophisticated|精密的} 设计。每一件家具都透露着主人的品味和地位。管家礼貌地引导她穿过长长的走廊，走廊两侧挂着价值不菲的艺术品。

"林小姐，老爷在书房等您。"管家的声音平静而 {meticulous|一丝不苟的}，每一个细节都处理得恰到好处。

林晚晚点了点头，心中却涌起一阵复杂的情绪。她从未想过，自己竟然会是这个 {prestigious|享有盛誉的} 家族的继承人。从小到大，她一直以为自己是普通家庭的孩子，直到三天前，一封律师函彻底改变了她的命运。

书房的门半开着，她轻轻敲了敲门。

"进来吧。"一个沉稳的声音从里面传来。

林晚晚推门而入，看到一位头发花白但精神矍铄的老人正坐在书桌前。他的眼神锐利而深邃，仿佛能看透一切。

"晚晚，你来了。"老人放下手中的文件，示意她坐下。"我知道这一切对你来说很突然，但这是你父亲生前的安排。"

"我父亲？"林晚晚的声音有些颤抖。

"是的，你的父亲林建国，是这个家族的真正继承人。他生前一直希望你能回来，继承这份家业。"老人的语气中带着一丝遗憾，"可惜，他走得太早了。"

林晚晚感到一阵眩晕。她从未见过自己的父亲，母亲也从未提起过。她一直以为父亲已经去世，或者根本不存在。

"我需要时间消化这一切。"她轻声说道。

"当然，这是人之常情。"老人点了点头，"但你要知道，这个家族需要你。你父亲留下的不仅仅是财富，更是一份责任。你需要变得足够 {ambitious|有野心的}，才能承担起这份重任。"

林晚晚看着老人，心中涌起一股从未有过的决心。也许，这就是她人生的转折点。她需要变得 {resilient|坚韧的}，需要学会在这个复杂的世界中生存。

"我会努力的。"她坚定地说道。`,
    },
    {
      id: "chapter-002",
      title: "第二章：新的开始",
      content: `一周后，林晚晚正式搬进了这座豪宅。她的房间被安排在二楼，窗外是精心打理的花园，四季常青的植物在微风中轻轻摇曳。

管家为她安排了专门的导师，开始系统地学习家族企业的运作方式。每天，她都要阅读大量的文件，了解公司的业务范围、财务状况以及未来的发展规划。

"林小姐，这是本季度的财务报表。"导师递给她一摞厚厚的文件，"您需要 {meticulous|一丝不苟的} 地审阅每一个细节，因为每一个数字都可能影响公司的未来。"

林晚晚接过文件，感到压力巨大。她从未接触过商业，更别说管理一家如此庞大的企业。但她知道，这是她必须面对的挑战。

"我会认真学习的。"她说道。

导师点了点头，眼中闪过一丝赞许。"很好，您有这样的态度，我相信您很快就能适应。记住，管理一家 {prestigious|享有盛誉的} 企业，需要的不仅仅是知识，更需要智慧和判断力。"

接下来的日子里，林晚晚几乎把所有时间都投入到学习中。她阅读商业案例，学习财务分析，了解市场动态。虽然过程艰难，但她从未想过放弃。

"晚晚，你最近很努力。"老人有一天在晚餐时对她说道，"但我希望你不要给自己太大压力。成长需要时间，你需要保持 {resilient|坚韧的} 心态，才能走得更远。"

"我知道。"林晚晚放下手中的餐具，"但我想要尽快适应这一切。我想要证明，我配得上这个位置。"

老人看着她，眼中闪过一丝欣慰。"你的父亲如果看到你现在这样，一定会很骄傲的。你和他一样，都有着 {ambitious|有野心的} 目标和坚定的意志。"

晚餐后，林晚晚回到自己的房间。她站在窗前，看着远处的城市灯火。这座城市，这个家族，这一切都是她从未想象过的。但她知道，这是她的新开始，是她必须走的路。

她打开电脑，开始制定自己的学习计划。她要用最 {sophisticated|精密的} 方法来提升自己，要用最 {elaborate|精心制作的} 方案来规划未来。

因为，她不仅仅是在继承一份家业，更是在书写属于自己的传奇。`,
    },
  ],
};


