# -*- coding:utf8 -*-
__author__ = 'Zovven'

import mistune


class TocMixin(object):
    """TOC mixin for Renderer, mix this with Renderer::
        class TocRenderer(TocMixin, Renderer):
            pass
        toc = TocRenderer()
        md = mistune.Markdown(renderer=toc)
        # required in this order
        toc.reset_toc()          # initial the status
        md.parse(text)           # parse for headers
        toc.render_toc(level=3)  # render TOC HTML
    """

    def reset_toc(self):
        self.toc_tree = []
        self.toc_count = 0

    def header(self, text, level, raw=None):
        rv = '<h%d id="toc-%d">%s</h%d>\n' % (
            level, self.toc_count, text, level
        )
        self.toc_tree.append((self.toc_count, text, level, raw))
        self.toc_count += 1
        return rv

    def render_toc(self):
        """Render TOC to HTML.
        :param level: render toc to the given level
        """
        return ''.join(self._iter_toc())

    def _iter_toc(self):
        last_level = None
        yield '<ul id="table-of-content">\n'
        for toc in self.toc_tree:
            index, text, l, raw = toc
            if l > 3 or l == 2:
                continue

            if l == 3 and last_level == 3:
                last_level = 3
                yield '</li>\n<li><a href="#toc-%d">%s</a>' % (index, text)
            elif l == 3 and last_level == 1:
                last_level = 3
                yield '<ul>\n<li><a href="#toc-%d">%s</a>' % (index, text)
            elif l == 1 and last_level == 3:
                last_level = 1
                yield '</li>\n</ul>\n</li>\n<li><a href="#toc-%d">%s</a>' % (index, text)
            elif l == 1 and last_level == 1:
                last_level = 1
                yield '</li>\n<li><a href="#toc-%d">%s</a>' % (index, text)
            elif l == 1:
                last_level = 1
                yield '<li><a href="#toc-%d">%s</a>' % (index, text)
            elif l == 3:
                last_level = 3
                yield '<li>\n<ul>\n<li><a href="#toc-%d">%s</a>' % (index, text)

        # close tags
        yield '</li>\n'
        if last_level == 3:
            yield '</ul>\n</li>\n'
        yield '</ul>\n'


class TocRenderer(TocMixin, mistune.Renderer):
    pass
