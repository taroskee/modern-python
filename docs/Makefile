# Minimal makefile for Sphinx documentation

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Custom targets
.PHONY: clean
clean:
	rm -rf $(BUILDDIR)/*
	rm -rf api/

.PHONY: apidoc
apidoc:
	sphinx-apidoc -f -o api ../src

.PHONY: livehtml
livehtml:
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" \
		--ignore "*.pyc" \
		--ignore "*.swp" \
		--ignore "*~" \
		--ignore ".git/*" \
		--ignore "_build/*" \
		--port 8888

.PHONY: linkcheck
linkcheck:
	$(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)/linkcheck"
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

.PHONY: doctest
doctest:
	$(SPHINXBUILD) -b doctest "$(SOURCEDIR)" "$(BUILDDIR)/doctest"
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in $(BUILDDIR)/doctest/output.txt."

.PHONY: coverage
coverage:
	$(SPHINXBUILD) -b coverage "$(SOURCEDIR)" "$(BUILDDIR)/coverage"
	@echo "Testing of coverage in the sources finished, look at the " \
	      "results in $(BUILDDIR)/coverage/python.txt."

.PHONY: watch
watch:
	while true; do \
		$(MAKE) html; \
		sleep 2; \
	done

.PHONY: serve
serve:
	@echo "Starting documentation server on http://localhost:8000"
	@cd $(BUILDDIR)/html && python -m http.server 8000