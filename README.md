# Zotero Paper Assistant

在网页端 ChatGPT 中检索本机 Zotero 文库，读取论文正文和原文页图。Zotero 文库通过本机只读 API 提供数据，ChatGPT 经私人隧道读取并在云端分析。

## 已配置的 Windows 电脑

1. 打开 Zotero，并保持私人隧道运行。电脑重启后，在资源管理器双击 `.local/tunnel-client/start-zotero-tunnel.cmd`，输入现有隧道 ID 和有效密钥。密钥在本机窗口隐藏输入。
2. 在 ChatGPT 对话里输入 `@`，选择 **Zotero Paper Assistant**。也可以从插件详情页点击 **在聊天中试用**。
3. 例如发送「在我的 Zotero 文库查找 RynnVLA-Latent，读取 PDF 第 1 页并报告全文页数」。精读图表时，可以要求查看对应的原文页图。

## 首次配置

1. 安装 Python 3.11 或更高版本，在项目目录运行 `python -m pip install -r requirements.txt`。在 Zotero 的 **设置 → 高级** 中允许本机应用通信。服务使用 `http://127.0.0.1:23119/api`。
2. 在 OpenAI Platform 建立私人 Secure MCP Tunnel。在同一组织创建 **Restricted** 运行密钥，为 **Tunnels** 授予 **Read** 和 **Use**。[官方权限说明](https://github.com/openai/tunnel-client/blob/master/docs/permissions.md#creating-keys)
3. 下载官方 Windows `tunnel-client`，从项目目录运行。将 MCP 目标设为 stdio 命令 `python -m zotero_agent.mcp_reader`，通过当前进程的 `CONTROL_PLANE_API_KEY` 提供运行密钥。运行 `doctor` 后启动隧道，并检查轮询状态。[官方隧道配置](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels)
4. 在 ChatGPT 插件目录添加自定义 MCP 服务器，连接类型选 **隧道**，填入隧道 ID。私人隧道内的服务选择 **无需身份验证**。创建后在聊天里试用，把样本论文的标题、DOI 和 PDF 页数与 Zotero 核对。[官方插件连接步骤](https://developers.openai.com/api/docs/guides/custom-mcp-server)

## 工具与验证

| 工具 | 用途 |
| --- | --- |
| `search_papers` | 按标题、DOI、arXiv ID 或作者搜索文献 |
| `get_paper` | 获取条目信息和 PDF 附件列表 |
| `read_pdf_pages` | 按 PDF 物理页码读取正文，每次最多 5 页 |
| `view_pdf_page` | 查看一页原文图像，适合核对公式、表格和扫描页 |

页码从 1 开始。安装依赖后运行 `python -m unittest discover -s tests -v` 检查本机代码。保持 `.local/` 和密钥在本机，提交前检查暂存内容。[Zotero 本地 API 说明](https://www.zotero.org/support/dev/web_api/v3/local_api)
