export const requireStatic = (str: any) => str

export const tooltip = (h: any, item: any, length: number = 13): any => {
    let texts = '' // 表格列显示文字
    if (item !== null) {
        if (item.length > length) { // 进行截取列显示字数
            texts = item.substring(0, length) + '...'
        } else {
            texts = item;
        }
    }
    return h('Tooltip', {
        props: {
            placement: 'top',
            transfer: true,
            // maxWidth: 150
        }
    }, [ // 这个中括号表示是Tooltip标签的子标签
        texts, // 表格列显示文字
        h('div', {
            slot: 'content',
            style: {
                whiteSpace: 'normal',
                wordBreak: 'break-all'
            }
        }, item) // 整个的信息即气泡内文字
    ])
}

// 删除空白字符
export const stripSpaceCharacter = (str: string): string => {
    return str.replace(/(^\s*)|(\s*$)/g, '')
}
